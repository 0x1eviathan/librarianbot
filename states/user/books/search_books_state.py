from api.database import db
from keyboards import search_books_markup, back_to_main_menu_markup

from main import user_router, bot

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class SearchBooks(StatesGroup):
    key_word = State()


@user_router.message(SearchBooks.key_word)
async def key_word_state(message: types.Message, state: FSMContext):
    key_word = message.text

    if key_word is None:
        raise Exception

    await message.delete()

    data = await state.get_data()

    message_id = data.get('message_id')

    chat_id = message.from_user.id

    searched_books = db.get_searched_books(book_owner=chat_id, key_word=key_word)

    if searched_books:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'<b> 🔎 Список найденных книг по Вашему запросу предостален снизу. :)</b>',
            reply_markup=search_books_markup(searched_books, key_word=key_word)
        )

        await state.clear()
    else:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'<b> ❗ К сожалению, мы ничего не нашли, попробуйте еще раз ввести запрос! :)</b>',
            reply_markup=back_to_main_menu_markup()
        )


