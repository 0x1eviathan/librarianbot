from api.database import db
from keyboards import close_message_markup

from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


# Обрабатываем каждый апдейт от человека и добавляем в бд, если его нет
class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        chat_id = event.from_user.id
        username = event.from_user.username

        user = db.get_user(chat_id=chat_id)

        if username is None:
            await event.delete()
            
            await event.answer(
                text='<b> 🧸 Укажите себе username в профиле, чтобы пользоваться нашим ботом. :) </b>',
                reply_markup=close_message_markup()
            )
            
            return False

        if user:
            if user.username != username: 
                user.username = username
                db.session_commit()
                
            return await handler(event, data)
        else:
            db.add_user(chat_id, username)
            
            return await handler(event, data)