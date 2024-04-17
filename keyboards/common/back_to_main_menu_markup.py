from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_main_menu_markup():
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='⬅️ Вернуться в меню',
            callback_data='back_to_main_menu'
        )
    )

    return builder.as_markup()
