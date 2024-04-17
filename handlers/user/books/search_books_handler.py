from api.database import db
from keyboards import (back_to_main_menu_markup, search_book_markup, search_books_markup, close_message_markup,
                       main_menu_markup)
from states import SearchBooks

from main import user_router

from aiogram import F, types
from aiogram.fsm.context import FSMContext


# Найти книгу по запросу
@user_router.callback_query(F.data == 'search_books')
async def search_books_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text(
        text=f'<b> 🔑 Введите ключевое слово, по которому я найду Вам книги в Вашей библиотеке! :) </b>',
        reply_markup=back_to_main_menu_markup()
    )

    message_id = message.message_id

    await state.update_data(message_id=message_id)

    await state.set_state(SearchBooks.key_word)


# Информация о найденной книге
@user_router.callback_query(F.data.startswith('searched_book'))
async def my_book_callback_handler(callback: types.CallbackQuery):
    book_id = int(callback.data.split(':')[1])
    key_word = callback.data.split(':')[2]

    my_book = db.get_my_book(book_id=book_id)

    book_name = my_book.book_name
    book_author = my_book.book_author
    book_description = my_book.book_description
    book_genre = my_book.book_genre

    await callback.message.edit_text(
        text=f'<b> 💡 Информацию о добавленной книге: </b> \n\n'
             f'<b> ✨ Название книги: {book_name} </b> \n'
             f'<b> ✍️ Автор книги: {book_author} </b> \n'
             f'<b> 📃 Описание книги: {book_description} </b> \n'
             f'<b> 🔮 Жанр книги: {book_genre} </b>',
        reply_markup=search_book_markup(book_id=book_id, key_word=key_word)
    )


# Возврат к найденным книгам по запросу
@user_router.callback_query(F.data.startswith('back_to_searched_books'))
async def back_to_searched_books_callback_handler(callback: types.CallbackQuery):
    key_word = callback.data.split(':')[1]

    chat_id = callback.from_user.id

    searched_books = db.get_searched_books(book_owner=chat_id, key_word=key_word)

    await callback.message.edit_text(
        text=f'<b> 🔎 Список найденных книг по Вашему запросу предостален снизу. :)</b>',
        reply_markup=search_books_markup(searched_books, key_word=key_word)
    )


# Удаление найденной книги из списка моих книг
@user_router.callback_query(F.data.startswith('delete_searched_book'))
async def delete_searched_book_callback_handler(callback: types.CallbackQuery):
    book_id = callback.data.split(':')[1]
    key_word = callback.data.split(':')[2]

    db.delete_my_book(book_id=book_id)

    await callback.message.edit_text(
        text='<b> ❌ Книга успешно удалена. </b>',
        reply_markup=close_message_markup()
    )

    chat_id = callback.from_user.id

    searched_books = db.get_searched_books(book_owner=chat_id, key_word=key_word)

    await callback.message.answer(
        text=f'<b> 🔎 Список найденных книг по Вашему запросу предостален снизу. :)</b>',
        reply_markup=search_books_markup(searched_books, key_word=key_word)
    )
