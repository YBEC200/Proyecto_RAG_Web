from app.services.laravel_client import LaravelClient
from app.services.vectorstore import VectorStoreService
from app.core.config import settings

TOKEN = "Bearer TU_TOKEN_ADMIN"

laravel = LaravelClient()
vectorstore = VectorStoreService()

products = laravel.get_products(TOKEN)

vectorstore.build_index(products)

print("✅ Índice FAISS generado correctamente")
