from main import common_router

from aiogram import F, types
from aiogram.fsm.context import FSMContext


# Удаление сообщения при нажатии на кнопку
@common_router.callback_query(F.data == 'close_message')
async def close_message_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    
    await callback.message.delete()
