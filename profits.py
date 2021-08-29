"""Работа с доходами - их добавление, удаление и статистика"""
import db
from categories import Categories
from typing import NamedTuple, Optional, List

import parser


class Profit(NamedTuple):
    """Структура добавленного в БД нового дохода"""
    id: Optional[int]
    profit: int
    category_name: str


def add_profit(raw_message: str) -> Profit:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = parser.parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    inserted_row_id = db.insert("profit", {
        "profit": parsed_message.profit,
        "created": parser.get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Profit(id=None,
                  profit=parsed_message.profit,
                  category_name=category.name)



def delete_profit(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    print('Собираюсь удалить')
    db.delete("profit", row_id)
    print("Удалил приьыль")


def get_today_statistics() -> str:
    """Возвращает строкой статистику доходов за сегодня"""
    cursor = db.get_cursor()
    cursor.execute("select sum(profit)"
                   "from profit where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "-------------------------------------------------\n"\
               "Что-тосегодня пока глухо...\n"\
               "-------------------------------------------------\n"
    all_today_profits = result[0]
    cursor.execute("select sum(profit) "
                   "from profit where date(created)=date('now', 'localtime') "
                   "and category_codename in (select codename "
                   "from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_profits = result[0] if result[0] else 0
    return ("-------------------------------------------------\n"
            f"Сегодня принесли в норку: {all_today_profits} руб.\n"
            "-------------------------------------------------\n"
            )


def get_month_statistics() -> str:
    """Возвращает строкой статистику расходов за текущий месяц"""
    now = parser.get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(profit) "
                   f"from profit where date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return ("-------------------------------------------------\n"
                "Пока в норку вы ничего не вносили\n"
                "-------------------------------------------------\n")
    all_today_profit = result[0]
    cursor.execute(f"select sum(profit) "
                   f"from profit where date(created) >= '{first_day_of_month}' "
                   f"and category_codename in (select codename "
                   f"from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_profit = result[0] if result[0] else 0
    return ("-------------------------------------------------\n"
            f"За этот месяц вы принесли в норку: {db.get_budget()} руб.\n"
            "-------------------------------------------------\n")


def last() -> List[Profit]:
    """Возвращает последние несколько расходов"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.profit, c.name "
        "from profit e left join category c "
        "on c.codename=e.category_codename "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_profits = [Profit(id=row[0], profit=row[1], category_name=row[2]) for row in rows]
    return last_profits
