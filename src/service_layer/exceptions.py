class UserServiceError(Exception):
    """Базовое исключение для UserService."""

    pass


class UserNotFoundError(UserServiceError):
    """Пользователь не найден (404)."""

    pass


class UserServiceUnavailableError(UserServiceError):
    """Сервис недоступен (5xx, таймаут и т.п.)."""

    pass
