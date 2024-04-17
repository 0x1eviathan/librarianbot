from api.database import db
from keyboards import main_menu_markup, close_message_markup, my_books_markup, my_book_markup, delete_my_book_markup

from main import user_router

from aiogram import types, F


# Список моих книг
@user_router.callback_query(F.data == 'my_books')
async def my_book_callback_handler(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    await callback.message.edit_text(
        text='<b> 👩🏻‍🏫 Список добавленных Вами книг. </b>',
        reply_markup=my_books_markup(chat_id=chat_id)
    )


# Список моих книг на определенной странице
@user_router.callback_query(F.data.startswith('with_page_my_books'))
async def with_page_my_books_callback_handler(callback: types.CallbackQuery):
    page = int(callback.data.split(':')[1])

    chat_id = callback.from_user.id

    await callback.message.edit_text(
        text='<b> 👩🏻‍🏫 Список добавленных Вами книг. </b>',
        reply_markup=my_books_markup(chat_id=chat_id, page=page)
    )


# Информация о моей книге
@user_router.callback_query(F.data.startswith('my_book'))
async def my_book_callback_handler(callback: types.CallbackQuery):
    book_id = callback.data.split(':')[1]
    page = callback.data.split(':')[2]

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
        reply_markup=my_book_markup(book_id=book_id, page=page)
    )


# Удалить книг
@user_router.callback_query(F.data.startswith('delete_my_book'))
async def delete_my_book_callback_handler(callback: types.CallbackQuery):
    book_id = callback.data.split(':')[1]
    page = int(callback.data.split(':')[2])

    await callback.message.edit_text(
        text='<b> ❌ Вы точно хотите удалить книгу из списка? </b>',
        reply_markup=delete_my_book_markup(book_id, page)
    )


# Подтвердить удаление книги
@user_router.callback_query(F.data.startswith('confirm_delete_my_book'))
async def confirm_delete_my_book_callback_handler(callback: types.CallbackQuery):
    book_id = callback.data.split(':')[1]

    db.delete_my_book(book_id=book_id)

    await callback.message.edit_text(
        text='<b> ❌ Книга успешно удалена. </b>',
        reply_markup=close_message_markup()
    )

    username = callback.from_user.username

    await callback.message.answer(
        text=f'<b> 📚 Добро пожаловать в библиотеку, @{username}! :) </b> \n\n'
             '<b> 🗃️ Чтобы пользоваться мною - используй кнопки снизу. </b>',
        reply_markup=main_menu_markup()
    )

# Хендлер элементов пагинации списка моих книг
@user_router.callback_query(F.data.startswith('pagination_my_books'))
async def pagination_my_books_callback_handler(callback: types.CallbackQuery):
    pagination_orientation = callback.data.split(':')[1]
    pagination_page = int(callback.data.split(':')[2])

    chat_id = callback.from_user.id

    if pagination_orientation == 'next':
        await callback.message.edit_reply_markup(
            reply_markup=my_books_markup(chat_id=chat_id, page=pagination_page + 1)
        )

    if pagination_orientation == 'back':
        await callback.message.edit_reply_markup(
            reply_markup=my_books_markup(chat_id=chat_id, page=pagination_page - 1)
        )
