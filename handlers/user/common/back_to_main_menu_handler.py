from keyboards import main_menu_markup

from main import user_router

from aiogram import F, types
from aiogram.fsm.context import FSMContext


# Возврат в меню
@user_router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    username = callback.from_user.username

    await callback.message.edit_text(
        text=f'<b> 📚 Добро пожаловать в библиотеку, @{username}! :) </b> \n\n'
             '<b> 🗃️ Чтобы пользоваться мною - используй кнопки снизу. </b>',
        reply_markup=main_menu_markup()

    )
