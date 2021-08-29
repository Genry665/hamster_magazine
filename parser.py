from config import list_expense
import datetime

import pytz
from typing import NamedTuple
import re


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Message1(NamedTuple):
    """Структура распаршенного сообщения о новом доходе"""
    profit: int
    category_text: str


def parse_message(raw_message: str) -> Message or Message1:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if regexp_result.group(2) in list_expense:
        amount = regexp_result.group(1).replace(" ", "")
        category_text = regexp_result.group(2).strip().lower()
        return Message(amount=amount, category_text=category_text)
    else:
        profit = regexp_result.group(1).replace(" ", "")
        category_text = regexp_result.group(2).strip().lower()
        return Message1(profit=profit, category_text=category_text)


def get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now
