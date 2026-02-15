from infrastructure.gigachat.chat import get_gigachat
from core.config import logger


class TelegramService:

    @classmethod
    async def get_start_message(cls) -> str:
        return "Привет!\n\nХотите узнать, чем знаменит Якутск? Я могу рассказать про достопримечательности, интересные маршруты и разные улицы.\n\nЧто вас интересует в первую очередь?"

    @classmethod
    async def process_client_message(cls, client_message: str, user_id: str) -> str:
        try:
            gigachat_service = get_gigachat()

            response = await gigachat_service.process_message(client_message, user_id)

            return response.content
        except Exception:
            logger.exception("Error occurred")
            return "К сожалению не удалось обработать ваш запрос, повторите позже. 😥"
