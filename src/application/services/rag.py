from io import BytesIO

from infrastructure.rag.storage import ChromaStorage
from infrastructure.rag.parser import ExcelDataParser


class RagService:
    def __init__(self):
        self.rag = ChromaStorage()

    async def parse_file(self, file: bytes):
        parser = ExcelDataParser()
        documents = parser.parse(file)

        await self.rag.save_documents(documents)

    async def clear_database(self):
        await self.rag.clear_database()

    async def get_documents_count(self) -> int:
        return self.rag.get_documents_count()

    async def search(self, query: str, limit: int = 10) -> str:
        return await self.rag.search(query, limit)


async def get_rag_service() -> RagService:
    return RagService()
