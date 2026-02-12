from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
import hashlib
import json

INDEX_PATH = Path("app/data/faiss_index")

class VectorStoreService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = None
        self.last_hash = None  # 👈 nuevo

    def _generate_hash(self, products: list[dict]) -> str:
        # Ordenamos para evitar cambios por orden distinto
        sorted_products = sorted(products, key=lambda x: x["id"])
        products_string = json.dumps(sorted_products, sort_keys=True)
        return hashlib.md5(products_string.encode()).hexdigest()

    def build_index_if_needed(self, products: list[dict]):
        current_hash = self._generate_hash(products)

        if self.last_hash == current_hash:
            # No hay cambios, no reconstruimos
            return

        # Si cambió, reconstruimos
        texts = []
        metadatas = []

        for p in products:
            text = (
                f"Nombre del producto: {p['nombre']}. "
                f"Marca: {p['marca']}. "
                f"Categoría: {p.get('categoria')}. "
                f"Descripción técnica: {p['descripcion']}."
            )

            texts.append(text)

            metadatas.append({
                "id": p["id"],
                "nombre": p["nombre"],
            })

        self.db = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )

        self.last_hash = current_hash
    
    
    def load(self):
        if INDEX_PATH.exists():
            self.db = FAISS.load_local(
                INDEX_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

    def search(self, query: str, k: int = 3):
        if not self.db:
            raise Exception("Índice no generado")

        return self.db.similarity_search(query, k=k)
