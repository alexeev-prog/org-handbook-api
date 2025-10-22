from pydantic_settings import BaseSettings

from orghandbookapi.config_loader import ConfigReader, ConfigType


class ConfigRunSectionModel(BaseSettings):
    """Модель конфигурации секции 'Run'."""

    host: str = "127.0.0.1"
    port: int = 8000


class ConfigDatabaseSectionModel(BaseSettings):
    """Модель конфигурации секции 'Database'."""

    host: str = "localhost"
    port: int = 5432
    name: str = "orghandbookapi"
    user: str = "admin"
    password: str = "password"  # noqa: S105
    url_format: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    expire_on_commit: bool = False


class ConfigSecuritySectionModel(BaseSettings):
    """Модель конфигурации секции 'Security'."""

    api_key: str = "secret-static-api-key"
    api_key_header: str = "X-API-Key"


class ConfigModel(BaseSettings):
    """Модель конфигурации."""

    run: ConfigRunSectionModel
    database: ConfigDatabaseSectionModel
    security: ConfigSecuritySectionModel


def load_config() -> ConfigModel:
    """
    Загрузка конфигурации в модель.

    Returns:
        ConfigModel: модель конфигурации

    """
    config_reader = ConfigReader("orghandbookapi.toml", ConfigType.TOML)
    return ConfigModel(**config_reader.config)


config = load_config()
