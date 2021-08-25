from aiogram import Bot, Dispatcher, executor, types
import expenses
import exceptions
import logging

from config import API_TOKEN


""" Настроить ведение журнала """
logging.basicConfig(level=logging.INFO)

""" Инициализировать бота и диспетчера """
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
class AddExpense:
    async def add_expense(self, message: types.Message):
        """Добавляет новый расход"""
        try:
            expense = expenses.add_expense(message.text)
        except exceptions.NotCorrectMessage as e:
            await message.answer(str(e))
            return
        answer_message = (
            f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
            f"{expenses.get_today_statistics()}")
        await message.answer(answer_message)


add_expense = AddExpense
