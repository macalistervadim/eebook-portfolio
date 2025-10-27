import logging

from src.config.loader import SettingsLoader
from src.config.settings import Settings
from src.exceptions import BootstrapInitializationError
from src.infrastructure.database.engine import get_engine
from src.infrastructure.logging.logger import configure_logging

logger = logging.getLogger(__name__)


async def bootstrap() -> Settings:
    try:
        configure_logging()
        await SettingsLoader().load()
        settings = Settings()  # type: ignore
        _ = get_engine()
        logger.info('Bootstrap успешно инициализировал компоненты')
        return settings

    except Exception as e:
        logger.exception('Bootstrap failed')
        raise BootstrapInitializationError(f'Failed to bootstrap application: {str(e)}') from e
