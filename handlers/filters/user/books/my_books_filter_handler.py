from filters import IsNotEmptyMyBooks

from main import user_router

from aiogram import F, types


# Обработка случая, когда фильтр проверки существования книг истинный
@user_router.callback_query(IsNotEmptyMyBooks(), F.data == 'my_books')
async def my_books_filter_callback_handler(callback: types.CallbackQuery):
    await callback.answer('В данный момент список Ваших книг пуст. :)')
