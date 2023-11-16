import re

import requests

counter_regex = re.compile(r'elem.innerHTML = "<span>(\d*)</span>', re.MULTILINE)

URL = 'https://miratermy.ru/'


def get_counter() -> int:
    """Получение счетчика с Мира Термы"""
    page = get_page()
    return parse_counter(page)


def get_page() -> str:
    """Получение страницы"""
    return requests.get(URL).text


def parse_counter(
        body: str,
) -> int:
    """Парсинг счетчика"""
    result = counter_regex.findall(body)
    return int(result[0])
