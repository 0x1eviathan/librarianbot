from keyboards import main_menu_markup

from main import user_router

from aiogram import filters, types


# CMD /START
@user_router.message(filters.CommandStart())
async def start_command_handler(message: types.Message):
    username = message.from_user.username

    await message.answer(
        text=f'<b> 📚 Добро пожаловать в библиотеку, @{username}! :) </b> \n\n'
             '<b> 🗃️ Чтобы пользоваться мною - используй кнопки снизу. </b>',
        reply_markup=main_menu_markup()
    )
