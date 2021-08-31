from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_back = KeyboardButton("Главное меню")
# Главное меню
button_minus = KeyboardButton('Расход')
button_plus = KeyboardButton('Прибыль')
button_budget = KeyboardButton("Бюджет")

main_menu1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_plus, button_minus, button_budget)

# Подменю расходов
button_today_expense = KeyboardButton('Сегодня потратили')
button_month_exp = KeyboardButton("Потратили за мясяц")
button_expenses = KeyboardButton("Последние траты")
button_categories = KeyboardButton("Категории")

menu_minus = ReplyKeyboardMarkup(resize_keyboard=True).add(button_today_expense,
                                                           button_month_exp,
                                                           button_expenses,
                                                           button_categories,
                                                           button_budget,
                                                           button_back)

# Доходы за сегодня
button_today_profit = KeyboardButton("Сегодня заработали")
button_month_prof = KeyboardButton("Заработки за месяц")
button_profits = KeyboardButton("Последние поступления")

menu_plus = ReplyKeyboardMarkup(resize_keyboard=True).add(button_today_profit,
                                                          button_month_prof,
                                                          button_profits,
                                                          button_back)