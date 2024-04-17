from api.database import db

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def search_books_markup(searched_books: list, key_word: str):
    builder = InlineKeyboardBuilder()

    for searched_book in searched_books:
        builder.add(
            types.InlineKeyboardButton(
                text=f'📚 {searched_book.book_name}',
                callback_data=f'searched_book:{searched_book.id}:{key_word}'
            )
        )

    builder.adjust(2)

    builder.row(
        types.InlineKeyboardButton(
            text='⬅️ Вернуться в меню',
            callback_data='back_to_main_menu'
        )
    )

    return builder.as_markup()


def search_book_markup(book_id: int, key_word: str):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='❌ Удалить книгу из списка',
            callback_data=f'delete_searched_book:{book_id}:{key_word}'
        ),
        types.InlineKeyboardButton(
            text='👩🏻‍🏫 Вернуться к списку книг',
            callback_data=f'back_to_searched_books:{key_word}'
        )
    )

    builder.adjust(1)

    return builder.as_markup()
