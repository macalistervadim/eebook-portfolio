import abc
from uuid import UUID

import httpx


class ABCUserService(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, user_id: UUID) -> dict | None:
        raise NotImplementedError


class UserSerivce(ABCUserService):
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def get_by_id(self, user_id: UUID) -> dict | None:
        async with httpx.AsyncClient(base_url=self._base_url, timeout=5.0) as client:
            resp = await client.get(f'api/v1/users/{user_id}')
            if resp.status_code != 200:
                return None
            return resp.json()
