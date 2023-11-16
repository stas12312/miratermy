from datetime import datetime

from consts import OPEN_TIME, CLOSE_TIME


def is_opened_time(
        now: datetime.time,
) -> bool:
    """Является ли время рабочим"""
    return CLOSE_TIME >= now >= OPEN_TIME
