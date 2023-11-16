import dataclasses
import enum
import os
from pathlib import Path
from typing import Self


class EnvField(enum.StrEnum):
    """Поля из переменных окружения"""
    CREDENTIALS_PATH = 'CREDENTIALS_PATH'
    SHEET_ID = 'SHEET_ID'


@dataclasses.dataclass
class Config:
    """Конфигурация скрипта"""
    credentials_path: Path
    sheet_id: str

    @classmethod
    def from_env(cls) -> Self:
        """Создание конфига из переменных окружения"""
        env = os.environ
        return cls(
            credentials_path=Path(env.get(EnvField.CREDENTIALS_PATH)),
            sheet_id=env.get(EnvField.SHEET_ID),
        )
