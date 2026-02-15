import base64

from langchain_gigachat import GigaChat
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

from core.config import get_settings
from infrastructure.rag.storage import ChromaStorage
from .prompt_manager import PromptManager

settings = get_settings()


def get_session_history(session_id: str):
    return RedisChatMessageHistory(
        url=settings.get_redis_url,
        session_id=session_id,
        ttl=settings.LLM_HISTORY_TTL,
    )


class GigachatService:

    def __init__(self, client_id: str, client_secret: str, scope: str):
        self.prompt_manager = PromptManager()
        self.rag = ChromaStorage()

        creds = f"{client_id}:{client_secret}".encode("utf-8")
        creds = base64.b64encode(creds).decode()

        self.llm = GigaChat(
            credentials=creds,
            scope=scope,
            verify_ssl_certs=False,
            model="GigaChat-2-Max",
            profanity_check=False,
            temperature=0.5,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.prompt_manager.get_prompt(agent_name=settings.LLM_AGENT_NAME),
                ),
                ("human", "{input}"),
            ]
        )

        chain = self.prompt | self.llm

        self.chain = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
        )

    async def process_message(self, message: str, user_id: str) -> AIMessage:
        context = await self.rag.search(message, limit=5)

        response = await self.chain.ainvoke(
            input={
                "input": message,
                "context": context,
            },
            config={
                "configurable": {
                    "session_id": f"{user_id}",
                }
            },
        )

        return response


def get_gigachat() -> GigachatService:
    return GigachatService(
        client_id=settings.GIGACHAT_CLIENT_ID,
        client_secret=settings.GIGACHAT_CLIENT_SECRET,
        scope=settings.GIGACHAT_SCOPE,
    )
