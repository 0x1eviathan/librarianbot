from api.database import db
from keyboards import (cancel_adding_book_markup, main_menu_markup, add_book_finish_markup, choose_my_genre_markup,
                       choose_book_genre, close_message_markup)
from states import AddBookState

from main import user_router, bot

from aiogram import types, F
from aiogram.fsm.context import FSMContext


# Процесс добавления книги в бд посредством перехода в состояние машины
@user_router.callback_query(F.data == 'add_book')
async def add_book_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    question_message = await callback.message.edit_text(
        text='<b> ✨ Напишите название Вашей книги. </b>',
        reply_markup=cancel_adding_book_markup()
    )

    question_message_id = question_message.message_id

    await state.update_data(question_message_id=question_message_id)

    await state.set_state(AddBookState.book_name)


# Добавление книги
@user_router.callback_query(F.data == 'add_book_finish')
async def add_book_finish_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id

    data = await state.get_data()

    book_name = data.get('book_name')
    book_author = data.get('book_author')
    book_description = data.get('book_description')
    book_genre = data.get('book_genre')

    db.add_book(chat_id, book_name, book_author, book_description, book_genre)

    await callback.message.edit_text(
        text='<b> ✅ Книга успешно добавлена. </b>',
        reply_markup=close_message_markup()
    )

    username = callback.from_user.username

    await callback.message.answer(
        text=f'<b> 📚 Добро пожаловать в библиотеку, @{username}! :) </b> \n\n'
             '<b> 🗃️ Чтобы пользоваться мною - используй кнопки снизу. </b>',
        reply_markup=main_menu_markup()
    )

    await state.clear()


# Возврат к выбору жанра
@user_router.callback_query(F.data == 'back_to_choose_genre')
async def back_to_choose_genre_callback_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text='<b> 🔮 Выберите жанр книги. </b>',
        reply_markup=choose_book_genre()
    )


# Выбор жанра
@user_router.callback_query(F.data.startswith('choose_genre'))
async def choose_genre_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    book_genre = callback.data.split(':')[1]

    if book_genre != 'my_genre':
        data = await state.get_data()

        book_name = data.get('book_name')
        book_author = data.get('book_author')
        book_description = data.get('book_description')

        await state.update_data(book_genre=book_genre)

        await callback.message.edit_text(
            text='<b> ✅ Добавить книгу? </b> \n\n'
                 f'<b> ✨ Название книги: <i>{book_name}</i> </b> \n'
                 f'<b> ✍️ Автор книги: <i>{book_author}</i> </b> \n'
                 f'<b> 📃 Описание книги: <i>{book_description}</i> </b> \n'
                 f'<b> 🔮 Жанр книги: <i>{book_genre}</i> </b>',
            reply_markup=add_book_finish_markup()
        )

    if book_genre == 'my_genre':
        data = await state.get_data()

        chat_id = callback.from_user.id
        question_message_id = data.get('question_message_id')

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text='<b> 🔮 Введите название своего жанра. </b>',
            reply_markup=choose_my_genre_markup()
        )

        await state.set_state(AddBookState.book_genre)


# Отмена добавления книги
@user_router.callback_query(F.data == 'cancel_adding_book')
async def cancel_adding_book_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    username = callback.from_user.username

    await callback.message.edit_text(
        text=f'<b> 📚 Добро пожаловать в библиотеку, @{username}! :) </b> \n\n'
             '<b> 🗃️ Чтобы пользоваться мною - используй кнопки снизу. </b>',
        reply_markup=main_menu_markup()
    )
