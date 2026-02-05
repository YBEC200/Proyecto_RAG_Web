from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import settings
from pathlib import Path

INDEX_PATH = Path("app/data/faiss_index")


class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY
        )

        if INDEX_PATH.exists():
            self.db = FAISS.load_local(
                INDEX_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            self.db = None

    def build_index(self, products: list[dict]):
        texts = []
        metadatas = []

        for p in products:
            text = (
                f"{p['nombre']} {p['marca']} "
                f"{p.get('descripcion', '')}"
            )
            texts.append(text)
            metadatas.append(p)

        self.db = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )

        INDEX_PATH.mkdir(parents=True, exist_ok=True)
        self.db.save_local(INDEX_PATH)

    def search(self, query: str, k: int = 5) -> list[dict]:
        if not self.db:
            return []

        docs = self.db.similarity_search(query, k=k)
        return [doc.metadata for doc in docs]
