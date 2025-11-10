import abc
import logging
from uuid import UUID

import httpx
import tenacity

from .exceptions import (
    UserNotFoundError,
    UserServiceError,
    UserServiceUnavailableError,
)

logger = logging.getLogger(__name__)

_RETRY_POLICY = tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    retry=tenacity.retry_if_exception_type((UserServiceUnavailableError, httpx.RequestError)),
    reraise=True,
)


class ABCUserService(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, user_id: UUID) -> dict:
        raise NotImplementedError


class UserService(ABCUserService):
    def __init__(self, base_url: str, max_retries: int = 3) -> None:
        self._base_url = base_url.rstrip('/')
        self._max_retries = max_retries

    @_RETRY_POLICY
    async def get_by_id(self, user_id: UUID) -> dict:
        """Получает данные пользователя по его идентификатору из внешнего микросервиса.

        Метод выполняет HTTP-запрос к внешнему сервису с автоматическими повторными
        попытками при временных сбоях (таймауты, 5xx ошибки). Поведение retry
        настраивается через tenacity.

        Args:
            user_id (UUID): Уникальный идентификатор пользователя.

        Returns:
            dict: JSON-представление пользователя, возвращённое внешним сервисом.

        Raises:
            UserNotFoundError: Если пользователь не найден (HTTP 404).
            UserServiceUnavailableError: Если сервис недоступен (таймаут, 5xx и т.п.).
            UserServiceError: При других неожиданных ошибках (например, 400, 401).

        Example:
            >>> service = UserService(base_url="https://api.example.com")
            >>> try:
            ...     user = await service.get_by_id(UUID("123e4567-e89b-12d3-a456-426614174000"))
            ...     print(user["name"])
            ... except UserNotFoundError:
            ...     print("Пользователь не существует")

        Note:
            Метод использует внутренний retry-механизм (tenacity) и не требует
            повторных вызовов со стороны клиента при временных ошибках.

        """
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=5.0) as client:
                resp = await client.get(f'/api/v1/users/{user_id}')

                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 404:
                    raise UserNotFoundError(f'Пользователь с ID {user_id} не найден')
                elif resp.status_code >= 500:
                    raise UserServiceUnavailableError(
                        f'User service вернул {resp.status_code}: {resp.text}',
                    )
                else:
                    raise UserServiceError(
                        f'Неизвестный статус {resp.status_code}'
                        f' для пользователя {user_id}: {resp.text}',
                    )

        except httpx.TimeoutException as e:
            logger.warning('Таймаут при запросе данных пользователя %s: %s', user_id, e)
            raise UserServiceUnavailableError('Таймаут запроса') from e

        except httpx.NetworkError as e:
            logger.exception('Сетевая ошибка при запросе пользователя %s: %s', user_id, e)
            raise UserServiceUnavailableError('Сетевая ошибка') from e

        except httpx.HTTPStatusError as e:
            logger.exception('Ошибка HTTP-статуса при запросе пользователя %s: %s', user_id, e)
            raise UserServiceError('Ошибка HTTP-ответа') from e
