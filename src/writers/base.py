import datetime
from typing import Protocol


class Writer(Protocol):
    """Протокол объекта записи"""

    def write(
            self,
            timestamp: datetime.datetime,
            value: int,
    ) -> None:
        """
        Запись значения
        :param timestamp: Отметка времени
        :param value: Записываемое значение
        :return:
        """
