from api.database import db

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choose_book_genre():
    builder = InlineKeyboardBuilder()

    genres = db.get_genres()

    for item in genres:
        builder.add(
            types.InlineKeyboardButton(
                text=f'{item.genre}',
                callback_data=f'choose_genre:{item.genre}'
            )
        )

    builder.adjust(2)

    builder.row(
        types.InlineKeyboardButton(
            text='🙋 Свой жанр',
            callback_data=f'choose_genre:my_genre'
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text='❌ Отменить добавление книги',
            callback_data='cancel_adding_book'
        )
    )

    return builder.as_markup()


def cancel_adding_book_markup():
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='❌ Отменить добавление книги',
            callback_data='cancel_adding_book'
        )
    )

    return builder.as_markup()


def add_book_finish_markup():
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='✔️ Добавить книгу',
            callback_data='add_book_finish'
        ),
        types.InlineKeyboardButton(
            text='⬅️ Вернуться к жанрам',
            callback_data='back_to_choose_genre'
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text='❌ Отменить добавление',
            callback_data='cancel_adding_book'
        )
    )

    return builder.as_markup()


def choose_my_genre_markup():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='⬅️ Вернуться к жанрам',
            callback_data='back_to_choose_genre'
        ),
        types.InlineKeyboardButton(
            text='❌ Отменить добавление книги',
            callback_data='cancel_adding_book'
        )
    )

    return builder.as_markup()
