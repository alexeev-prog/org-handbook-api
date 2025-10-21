from pydantic_settings import BaseSettings

from orghandbookapi.config_loader import ConfigReader, ConfigType


class ConfigRunSectionModel(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class ConfigDatabaseSectionModel(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    name: str = "orghandbookapi"
    user: str = "admin"
    password: str = "password"
    url_format: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    expire_on_commit: bool = False


class ConfigSecuritySectionModel(BaseSettings):
    api_key: str = "secret-static-api-key"
    api_key_header: str = "X-API-Key"


class ConfigModel(BaseSettings):
    run: ConfigRunSectionModel
    database: ConfigDatabaseSectionModel
    security: ConfigSecuritySectionModel


def load_config() -> ConfigModel:
    config_reader = ConfigReader("orghandbookapi.toml", ConfigType.TOML)
    return ConfigModel(**config_reader.config)


config = load_config()
