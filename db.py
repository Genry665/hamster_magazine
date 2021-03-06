import os
import sqlite3

from typing import Dict, List, Tuple

conn = sqlite3.connect(os.path.join("db", "test.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def get_budget():
    budget_select = """SELECT * from budget"""
    cursor.execute(budget_select)
    total_budget = cursor.fetchone()
    for budget in total_budget:
        return budget


def add_profit(add_profit):
    budget = get_budget()
    total = budget + add_profit
    cursor.execute(f"UPDATE budget SET budget={total} where id=1")
    conn.commit()


def minus_expense(min_expense):
    budget = get_budget()
    total = budget - min_expense
    cursor.execute(f"UPDATE budget SET budget={total} where id=1")
    conn.commit()


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    budget = get_budget()
    if table == 'expense':
        cursor.execute(f"SELECT amount FROM {table} WHERE id={row_id}")
        amount = cursor.fetchone()
        total = budget + amount[0]
        cursor.execute(f"UPDATE budget SET budget={total} where id=1")
    else:
        cursor.execute(f"SELECT profit FROM {table} WHERE id={row_id}")
        profit = cursor.fetchone()
        total = budget - profit[0]
        cursor.execute(f"UPDATE budget SET budget={total} where id=1")
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor
