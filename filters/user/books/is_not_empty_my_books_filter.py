from api.database import db

from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


# Проверка существования какой-либо книги у пользователя
class IsNotEmptyMyBooks(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        chat_id = message.from_user.id

        my_books = db.get_my_books(chat_id=chat_id)

        if not my_books:
            return True

        return False
