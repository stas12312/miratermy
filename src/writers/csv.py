import csv
import datetime

from .utils import TIME_FORMAT


class CSVWriter:
    """Запись данных в CSV файл"""

    @staticmethod
    def write(
            dt: datetime.datetime,
            value: int,
    ) -> None:
        """Запись данных в CSV файл"""
        time_title = dt.time().strftime(TIME_FORMAT)
        filename = dt.date().isoformat()

        with open(f'{filename}.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time_title, value])
