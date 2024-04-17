import math

from api.database import db

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def my_books_markup(chat_id, page=1, items_per_page=3):
    builder = InlineKeyboardBuilder()

    start_item = (page - 1) * items_per_page
    end_item = start_item + items_per_page

    my_books = db.get_my_books(chat_id=chat_id)

    buttons = []

    for my_book in my_books[start_item:end_item]:
        buttons.append(
            types.InlineKeyboardButton(
                text=f'📚 {my_book.book_name}',
                callback_data=f'my_book:{my_book.id}:{page}'
            )
        )

    builder.add(*buttons)

    builder.adjust(2)

    if len(my_books) > 6:
        if page == 1:
            builder.row(
                types.InlineKeyboardButton(
                    text=f'{page} / {math.ceil(len(my_books) / items_per_page)}',
                    callback_data='#'
                ),
                types.InlineKeyboardButton(
                    text=f'➡',
                    callback_data=f'pagination_my_books:next:{page}'
                )
            )
        if page > 1 and page == math.ceil(len(my_books) / items_per_page):
            builder.row(
                types.InlineKeyboardButton(
                    text=f'⬅',
                    callback_data=f'pagination_my_books:back:{page}'
                ),
                types.InlineKeyboardButton(
                    text=f'{page} / {math.ceil(len(my_books) / items_per_page)}',
                    callback_data='#'
                )
            )
        if 1 < page < math.ceil(len(my_books) / items_per_page):
            builder.row(
                types.InlineKeyboardButton(
                    text=f'⬅',
                    callback_data=f'pagination_my_books:back:{page}'
                ),
                types.InlineKeyboardButton(
                    text=f'{page} / {math.ceil(len(my_books) / items_per_page)}',
                    callback_data='#'
                ),
                types.InlineKeyboardButton(
                    text=f'➡',
                    callback_data=f'pagination_my_books:next:{page}'
                )
            )

    builder.row(
        types.InlineKeyboardButton(
            text='⬅️ Вернуться в меню',
            callback_data='back_to_main_menu'
        )
    )

    return builder.as_markup()


def my_book_markup(book_id, page=1):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='❌ Удалить книгу из списка',
            callback_data=f'delete_my_book:{book_id}:{page}'
        ),
    )

    if int(page) > 1:
        builder.add(
            types.InlineKeyboardButton(
                text='👩🏻‍🏫 Вернуться к списку моих книг',
                callback_data=f'with_page_my_books:{page}'
            )
        )
    else:
        builder.add(
            types.InlineKeyboardButton(
                text='👩🏻‍🏫 Вернуться к списку моих книг',
                callback_data=f'my_books'
            )
        )

    builder.adjust(1)

    return builder.as_markup()


def delete_my_book_markup(book_id: int, page: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='✅ Подтвердить',
            callback_data=f'confirm_delete_my_book:{book_id}'
        ),
        types.InlineKeyboardButton(
            text='⬅️ Вернуться назад',
            callback_data=f'my_book:{book_id}:{page}'
        )
    )

    return builder.as_markup()
