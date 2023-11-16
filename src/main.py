import datetime

from apscheduler.schedulers.background import BlockingScheduler

from config import Config
from consts import OPEN_TIME
from parser import get_counter
from utils import is_opened_time
from writer import write_counter
from writers import GoogleSheetsWriter, CSVWriter
from writers.base import Writer


def processing_counter(
        writers: list[Writer],
) -> None:
    """Парсинг и запись счетчика"""

    # Запускаем парсинг только в рабочее время
    now = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=7)
    if not is_opened_time(now.time()):
        return

    counter = get_counter()
    write_counter(now, writers, counter)


def main() -> None:
    """Точка входа"""
    config = Config.from_env()
    writers = [
        GoogleSheetsWriter(config.sheet_id, config.credentials_path, OPEN_TIME),
        CSVWriter(),
    ]
    scheduler = BlockingScheduler()
    scheduler.add_job(processing_counter, 'interval', [writers], minutes=1)
    scheduler.start()


if __name__ == '__main__':
    main()
