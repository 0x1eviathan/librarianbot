from api.database import db
from keyboards import cancel_adding_book_markup, choose_book_genre, add_book_finish_markup, choose_my_genre_markup

from main import bot, user_router

from aiogram import types, filters, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class AddBookState(StatesGroup):
    book_name = State()
    book_author = State()
    book_description = State()
    book_genre = State()


# Состояния машин для сбора информации о книге

@user_router.message(AddBookState.book_name)
async def book_name_state(message: types.Message, state: FSMContext):
    try:
        book_name = message.text

        if book_name is None:
            raise Exception

        chat_id = message.from_user.id

        check_book = db.check_book(book_owner=chat_id, book_name=book_name)

        if check_book:
            await message.delete()

            data = await state.get_data()

            chat_id = message.from_user.id
            question_message_id = data.get('question_message_id')

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=question_message_id,
                text=f'<b> 🛑 Книга с таким названием уже существует в Вашей библиотеке. </b> \n\n'
                     f'<b> ✨ Напишите название Вашей книги. </b>',
                reply_markup=cancel_adding_book_markup()
            )

            return

        await state.update_data(book_name=book_name)

        await message.delete()

        data = await state.get_data()

        question_message_id = data.get('question_message_id')

        question_message = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text='<b> ✍️ Напишите инициалы автора. </b>',
            reply_markup=cancel_adding_book_markup()
        )

        question_message_id = question_message.message_id

        await state.update_data(question_message_id=question_message_id)

        await state.set_state(AddBookState.book_author)
    except Exception as e:
        print(e)

        await message.delete()

        data = await state.get_data()

        chat_id = message.from_user.id
        question_message_id = data.get('question_message_id')

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text=f'<b> 🛑 Недопустимое значение! Попробуйте повторить. </b> \n\n'
                 f'<b> ✨ Напишите название Вашей книги. </b>',
            reply_markup=cancel_adding_book_markup()
        )

        return


@user_router.message(AddBookState.book_author)
async def book_name_state(message: types.Message, state: FSMContext):
    try:
        book_author = message.text

        if book_author is None:
            raise Exception

        await state.update_data(book_author=book_author)

        await message.delete()

        chat_id = message.from_user.id

        data = await state.get_data()

        question_message_id = data.get('question_message_id')

        question_message = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text='<b> 📃 Напишите краткое описание книги. </b>',
            reply_markup=cancel_adding_book_markup()
        )

        question_message_id = question_message.message_id

        await state.update_data(question_message_id=question_message_id)

        await state.set_state(AddBookState.book_description)
    except Exception as e:
        print(e)

        await message.delete()

        data = await state.get_data()

        chat_id = message.from_user.id
        question_message_id = data.get('question_message_id')

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text=f'<b> 🛑 Недопустимое значение! Попробуйте повторить. </b> \n\n'
                 f'<b> ✍️ Напишите инициалы автора. </b>',
            reply_markup=cancel_adding_book_markup()
        )

        return


@user_router.message(AddBookState.book_description)
async def book_name_state(message: types.Message, state: FSMContext):
    try:
        book_description = message.text

        if book_description is None:
            raise Exception

        await state.update_data(book_description=book_description)

        await message.delete()

        chat_id = message.from_user.id

        data = await state.get_data()

        question_message_id = data.get('question_message_id')

        question_message = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text='<b> 🔮 Выберите жанр книги. </b>',
            reply_markup=choose_book_genre()
        )

        question_message_id = question_message.message_id

        await state.update_data(question_message_id=question_message_id)
    except Exception as e:
        print(e)

        await message.delete()

        data = await state.get_data()

        chat_id = message.from_user.id
        question_message_id = data.get('question_message_id')

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text=f'<b> 🛑 Недопустимое значение! Попробуйте повторить. </b> \n\n'
                 f'<b> 📃 Напишите краткое описание книги. </b>',
            reply_markup=cancel_adding_book_markup()
        )

        return


@user_router.message(AddBookState.book_genre)
async def book_genre_state(message: types.Message, state: FSMContext):
    try:
        book_genre = message.text

        if book_genre is None:
            raise Exception

        await message.delete()

        chat_id = message.from_user.id

        data = await state.get_data()

        chat_id = message.from_user.id
        question_message_id = data.get('question_message_id')

        book_name = data.get('book_name')
        book_author = data.get('book_author')
        book_description = data.get('book_description')

        question_message = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text='<b> ✅ Добавить книгу? </b> \n\n'
                 f'<b> ✨ Название книги: <i>{book_name}</i> </b> \n'
                 f'<b> ✍️ Автор книги: <i>{book_author}</i> </b> \n'
                 f'<b> 📃 Описание книги: <i>{book_description}</i> </b> \n'
                 f'<b> 🔮 Жанр книги: <i>{book_genre}</i> </b>',
            reply_markup=add_book_finish_markup()
        )

        question_message_id = question_message.message_id

        await state.update_data(book_genre=book_genre, question_message_id=question_message_id)
    except Exception as e:
        print(e)

        await message.delete()

        data = await state.get_data()

        chat_id = message.from_user.id
        question_message_id = data.get('question_message_id')

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=question_message_id,
            text=f'<b> 🛑 Недопустимое значение! Попробуйте повторить. </b> \n\n'
                 f'<b> 🔮 Введите название своего жанра. </b>',
            reply_markup=choose_my_genre_markup()
        )

        return
