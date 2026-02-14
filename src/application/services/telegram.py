class TelegramService:

    @classmethod
    async def get_start_message(cls) -> str:
        return "Привет!\n\nХотите узнать, чем знаменит Якутск? Я могу рассказать про достопримечательности, интересные маршруты и разные улицы.\n\nЧто вас интересует в первую очередь?"

    @classmethod
    async def process_client_message(cls, client_message: str) -> str:
        return "PONG"
