from aiogram import Router, types
from aiogram.filters import CommandStart

from application.services.telegram import TelegramService

router = Router()

telegram_service = TelegramService()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(await telegram_service.get_start_message())


@router.message()
async def echo(message: types.Message):
    user_id = message.from_user.id
    response = await telegram_service.process_client_message(
        client_message=message.text, user_id=str(user_id)
    )

    await message.answer(response)
