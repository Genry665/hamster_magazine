import re
import exceptions

from typing import NamedTuple
from config import list_expense


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
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не не, пиши так...\n "
            "1500 метро\n"
            "P.S. твой Хомяк :*")
    if regexp_result.group(2) in list_expense:
        amount = regexp_result.group(1).replace(" ", "")
        category_text = regexp_result.group(2).strip().lower()
        print(type(category_text), 'это кат messagw')
        print(regexp_result.group(2), 'это парсер')
        return Message(amount=amount, category_text=category_text)
    else:
        profit = regexp_result.group(1).replace(" ", "")
        category_text = regexp_result.group(2).strip().lower()
        print(Message1, "666")
        print(regexp_result.group(2))
        return Message1(profit=profit, category_text=category_text)
