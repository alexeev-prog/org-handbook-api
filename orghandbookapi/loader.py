from pydantic import BaseSettings
from orghandbookapi.config_loader import ConfigReader, ConfigType


class ConfigRunSectionModel(BaseSettings):
    host: str
    port: int


class ConfigDatabaseSectionModel(BaseSettings):
    host: str
    port: str
    name: str
    user: str
    password: str
    url_format: str


class ConfigSecuritySectionModel(BaseSettings):
    api_key: str
    api_key_header: str


class ConfigModel(BaseSettings):
    run: ConfigRunSectionModel
    database: ConfigDatabaseSectionModel
    security: ConfigSecuritySectionModel


def load_config() -> ConfigModel:
    config_reader = ConfigReader("orghandbookapi.toml", ConfigType.TOML)

    return ConfigModel(config_reader.config)


config = load_config()
