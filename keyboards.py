from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def reply_keyboard(*buttons):
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.button(text=button)
    return builder.as_markup(resize_keyboard=True)