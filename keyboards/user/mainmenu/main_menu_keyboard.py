from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_markup():
    builder = InlineKeyboardBuilder()

    buttons = [
        types.InlineKeyboardButton(
            text='➕ Добавить книгу',
            callback_data='add_book'
        ),
        types.InlineKeyboardButton(
            text='📋 Мой список книг',
            callback_data='my_books'
        ),
        types.InlineKeyboardButton(
            text='🔎 Поиск книги',
            callback_data='search_books'
        )
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(2)

    return builder.as_markup()
