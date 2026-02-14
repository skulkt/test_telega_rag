from aiogram import Bot, Dispatcher
from core import config

from .handlers import router

settings = config.get_settings()

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()


async def start_pooling():
    dp.include_router(router)

    await dp.start_polling(bot)
