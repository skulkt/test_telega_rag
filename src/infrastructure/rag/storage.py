from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from core.config import get_settings

settings = get_settings()


class ChromaStorage:
    def __init__(self):
        self.persist_dir = "/code/chroma.db"
        self.embeddings = HuggingFaceEmbeddings(
            model_name=f"/code/models/{settings.SENTENCES_MODEL_DIR}",
            model_kwargs={"device": "cpu"},
        )

        self._storage = None

    @property
    def storage(self):
        if self._storage is None:
            self._storage = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
            )

        return self._storage

    async def save_documents(self, documents: list[Document]):
        await self.storage.aadd_documents(documents)

    async def clear_database(self):
        self.storage.delete_collection()
        self._storage = None

    def get_documents_count(self) -> int:
        return len(self.storage.get()["ids"])

    async def search(self, query: str, limit: int = 10) -> str:
        docs = await self.storage.asimilarity_search(query, k=limit)

        return "\n\n===\n\n".join([doc.page_content for doc in docs])
