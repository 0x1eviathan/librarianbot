import asyncio
import logging

from api.database import db
from handlers import common_router, user_router

from main import bot

from aiogram import Dispatcher


async def on_startup():
    db.create_tables()


async def main(): 
    await on_startup() 
    
    # //////////////////////
    
    dp = Dispatcher() 
    
    # //////////////////////
    
    dp.include_routers(common_router, user_router)
    
    # //////////////////////
    
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
