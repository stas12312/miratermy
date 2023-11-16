import datetime

from consts import OPEN_TIME, CLOSE_TIME
from writers.base import Writer


def write_counter(
        dt: datetime.datetime,
        writers: list[Writer],
        value: int,
) -> None:
    """Запись значения"""
    for writer in writers:
        writer.write(dt, value)
