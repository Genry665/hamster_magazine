import re
import exceptions

from typing import NamedTuple


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
    if regexp_result.group(2) == "+":
        profit = regexp_result.group(1).replace(" ", "")
        category_text = regexp_result.group(2).strip().lower()
        print(Message1, "555")
        return Message1(profit=profit, category_text=category_text)
    else:
        amount = regexp_result.group(1).replace(" ", "")
        category_text = regexp_result.group(2).strip().lower()
        print(Message, "666")
        return Message(amount=amount, category_text=category_text)
