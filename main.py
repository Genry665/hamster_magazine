import logging
from config import API_TOKEN, Msr_An, Mr_Sir, list_expense
import db

from aiogram import Bot, Dispatcher, executor, types

import re

import exceptions
import expenses
import profits
from categories import Categories

""" Настроить ведение журнала """
logging.basicConfig(level=logging.INFO)

""" Инициализировать бота и диспетчера """
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    async def wrapper(message):
        if message['from']['id'] != Mr_Sir:
            if message['from']['id'] != Msr_An:
                return await message.reply("Не для тебя хомячок старается!", reply=False)
        if message['from']['id'] == Mr_Sir:
            return await func(message, name='Господин!')
        else:
            return await func(message, name='Госпожа!')

    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def send_welcome(message: types.Message, name='', name1=""):
    """Этот обработчик будет вызываться, когда пользователь отправит команду `/ start` или` / help`."""
    await message.answer(
        f"Ваш хомяк для учета финансов приветствует вас {name}!\n\n"
        f"Что желает {name1} {name}?\n"
        "-------------------------------------------------\n"
        "Добавить расход: /minus\n"
        "Или добавить прибыль: /plus\n"
        "-------------------------------------------------"
    )


class MainMenu:
    """Логика главного меню"""

    def __init__(self, name_table, name_category, rus_name, rus_names, today, month):
        self.name_table = name_table
        self.name_category = name_category
        self.rus_name = rus_name
        self.rus_names = rus_names
        self.today = today
        self.month = month

    def send_message(self):
        """Формирет ворую ветку меню"""
        message_menu = (
            f"добавить {self.rus_name}: /{self.name_table}\n"
            f"Сегодняшняя статистика : /{self.today}\n"
            f"Статистика за месяц: /{self.month}\n"
            f"Последние внесённые {self.rus_names}: /{self.name_category}\n"
            "Категории: /categories\n"
            "Бюджет: /budget\n"
        )
        return message_menu


Main_minus = MainMenu("expense", "expenses", "расход", "расходы", 'today_expense', "month_exp")

Main_plus = MainMenu("profit", "profits", "доход", "доходы", 'today_profit', "month_prof")


@dp.message_handler(commands=['minus'])
async def get_plus_message(message: types.Message):
    await message.answer(Main_minus.send_message())


@dp.message_handler(commands=['plus'])
async def get_main_menu(message: types.Message):
    await message.answer(Main_plus.send_message())


@dp.message_handler(lambda message: message.text.startswith('/udalyl'))
async def del_profit(message: types.Message):
    """Удаляет одну запись о доходе по её индентификатору"""
    print("Удаляю прибыль22222")
    row_id = int(message.text[7:])
    profits.delete_profit(row_id)
    answer_message = 'Как будто и не было...'
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории для ввода:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['budget'])
async def budget(message: types.Message):
    """Вывод текущего бюджета"""
    total_budget = db.get_budget()
    answer_message = f"Сейчас в норке: {total_budget} рублей"
    await message.answer(answer_message)


@dp.message_handler(commands=['today_expense'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_exp'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler(commands=['today_profit'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику поподнений"""
    answer_message = profits.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_prof'])
async def month_statistics(message: types.Message):
    """Отправляет статистику пополнений текущего месяца"""
    answer_message = profits.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['profits'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о доходах"""
    last_profits = profits.last()
    if not last_profits:
        await message.answer("Доходы ещё не заведены")
        return
    last_profits_rows = [
        f"{profit.profit} руб. на {profit.category_name} — нажми "
        f"/udalyl{profit.id} для удаления"
        for profit in last_profits]
    answer_message = "Последние сохранённые прибыли:\n\n* " + "\n\n* " \
        .join(last_profits_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_doing(message: types.Message):
    """Добавляет новый расход/доход"""
    full_message = re.match(r"([\d ]+) (.*)", message.text)
    try:
        message_category = full_message.group(2).strip().lower()
        if int(full_message.group(1).replace(" ", "")) != 0:
            if message_category in list_expense:
                try:
                    expense = expenses.add_expense(message.text)
                    min_expense = db.minus_expense(int(full_message.group(1).replace(" ", "")))
                except exceptions.NotCorrectMessage as e:
                    await message.answer(str(e))
                    return
                answer_message = (
                    f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
                    f"{expenses.get_today_statistics()}")
                await message.answer(answer_message)
            else:
                try:
                    profit = profits.add_profit(message.text)
                    add_profit = db.add_profit(int(full_message.group(1).replace(" ", "")))
                except exceptions.NotCorrectMessage as e:
                    await message.answer(str(e))
                    return
                answer_message = (
                    f"Добавлены прибыль {profit.profit} руб.\n\n"
                    f"{profits.get_today_statistics()}")
                await message.answer(answer_message)
        else:
            await message.answer("Совсем не так!\n"
                                 "Сначала число, потом категория\n"
                                 "К примеру: 500 коты\n\n"
                                 "С уважением, твой Хомяк.")
    except AttributeError:
        await message.answer("Совсем не так!\n"
                             "Сначала число, потом категория\n"
                             "К примеру: 500 коты\n\n"
                             "С уважением, твой Хомяк.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
