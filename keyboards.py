from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_kb(*buttons):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in buttons:
        markup.add(item)
    return markup