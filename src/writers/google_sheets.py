import datetime
from pathlib import Path
from typing import NamedTuple

import pygsheets
from pygsheets import Cell, WorksheetNotFound, Worksheet

from .utils import NAME_BY_MONTH_NUMBER, NAME_BY_DAY_NUMBER, TIME_FORMAT


class CellIndex(NamedTuple):
    """Индекс ячейки"""
    row: int
    column: int


class GoogleSheetsWriter:
    """Класс записи в Google таблицу"""

    def __init__(
            self,
            sheet_id: str,
            credentials_path: Path,
            start_time: datetime.time,
    ) -> None:
        self._sheet_id = sheet_id
        self._gc = pygsheets.authorize(service_file=credentials_path)
        self._start_time = start_time

    def write(
            self,
            dt: datetime.datetime,
            value: int,
    ) -> None:
        """Запись значения в Google таблицу"""
        sheet_name = dt.date().strftime('%Y-%m')
        work_sheet = self._get_worksheet(sheet_name)
        cell_index = self.get_index(work_sheet, dt)
        cell = work_sheet.cell(cell_index)
        cell.value = value

    def _get_worksheet(
            self,
            name: str,
    ) -> Worksheet:
        """Получение рабочего листа"""
        sh = self._gc.open_by_key(self._sheet_id)
        try:
            ws = sh.worksheet_by_title(name)
        except WorksheetNotFound:
            print(f'Создание листа {name}')
            ws = sh.add_worksheet(name, rows=1000, cols=32, index=0)
            ws.update_row(1, ['Время'])
        return ws

    def get_index(
            self,
            ws: Worksheet,
            dt: datetime.datetime,
    ) -> CellIndex:
        """Получение индекса для записи"""
        column_title = get_column_title(dt)

        cells = ws.get_all_values('cell')
        row = self.get_row(cells, dt.time())
        column = get_column(cells, column_title)

        return CellIndex(row, column)

    def get_row(
            self,
            cells: list[list[Cell]],
            time: datetime.time,
    ) -> int:
        """Получение номера строки для записи"""
        mark = time.hour * 60 + time.minute
        row = mark - time_to_minutes(self._start_time) + 2
        if row <= 1:
            raise ValueError('Некорректный индекс времени')

        cell = cells[row - 1][0]
        title = time.strftime(TIME_FORMAT)
        if cell.value != title:
            cell.value = title

        return row


def get_column(
        cells: list[list[Cell]],
        title: str,
) -> int:
    """Получение номера колонки для записи"""
    first_row = cells[0]
    for i, cell in enumerate(first_row, start=1):
        value = cell.value
        if not value:
            cell.value = title
            return i
        if value == title:
            return i


def time_to_minutes(
        time: datetime.time,
) -> int:
    """Получение времени в минутах"""
    return time.hour * 60 + time.minute


def get_column_title(
        dt: datetime.datetime | datetime.date,
) -> str:
    """Получение заголовка для столбца"""
    day = dt.day
    month_name = NAME_BY_MONTH_NUMBER[dt.month - 1]
    day_name = NAME_BY_DAY_NUMBER[dt.weekday()]

    return f'{day} {month_name} ({day_name})'
