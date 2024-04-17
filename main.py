from middlewares import UserMiddleware

from config import settings

from aiogram import Bot, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode


# /////////// MAIN SECTION ///////////

bot_token = settings['bot_token']
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# /////////// ROUTERS ///////////

common_router = Router()

user_router = Router() 
user_router.message.outer_middleware(UserMiddleware())
