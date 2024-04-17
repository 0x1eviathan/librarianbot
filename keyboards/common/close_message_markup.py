from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def close_message_markup():
    builder = InlineKeyboardBuilder() 
    
    builder.add(
        types.InlineKeyboardButton(
            text='🗑️ Убрать сообщение',
            callback_data='close_message'
        )
    )
    
    return builder.as_markup()
