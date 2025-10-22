from enum import Enum
from pathlib import Path

import orjson as json
import toml
import yaml


class ConfigType(Enum):
    """Типы конфигурационных файлов."""

    TOML = 0
    YAML = 1
    JSON = 2


def detect_config_type_by_extension(extension: str) -> ConfigType:
    """
    Обнаружение типа конфигурации по расширению файла.

    Args:
        extension (str): расширение файла

    Returns:
        ConfigType: тип конфигурации

    """
    cleaned_extension = extension.lower().lstrip(".")

    if cleaned_extension == "json":
        return ConfigType.JSON
    if cleaned_extension in ("yaml", "yml"):
        return ConfigType.YAML
    if cleaned_extension == "toml":
        return ConfigType.TOML
    return ConfigType.JSON


def detect_config_type_by_filename(filename: str) -> ConfigType:
    """
    Обнаружение типа конфигурации по файлу.

    Args:
        filename (str): имя файла

    Returns:
        ConfigType: тип конфигурации

    """
    extension = Path(filename).suffix.lstrip(".") or filename
    return detect_config_type_by_extension(extension)


class ConfigReader:
    """Класс, реализующий чтение конфигурационного файла."""

    def __init__(self, config_file: str, configtype: ConfigType = None):
        """
        Инициализация класса.

        Args:
            config_file (str): файл конфигурации
            configtype (ConfigType, optional): тип конфигурации. По умолчанию None.

        """
        self.config_file: Path = Path(config_file)

        if configtype is None:
            self.configtype: ConfigType = detect_config_type_by_filename(config_file)
        else:
            self.configtype: ConfigType = configtype

        self.config: dict[str, any] = self._load_data_from_config()

    def _load_data_from_config(self) -> dict:
        data = {}

        if not self.config_file.exists():
            return data

        if self.configtype == ConfigType.YAML:
            with self.config_file.open() as f:
                data = yaml.safe_load(f)
        elif self.configtype == ConfigType.TOML:
            with self.config_file.open() as f:
                data = toml.load(f)
        elif self.configtype == ConfigType.JSON:
            with self.config_file.open("rb") as f:
                data = json.loads(f.read())

        return data if isinstance(data, dict) else {}
