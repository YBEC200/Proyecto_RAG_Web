from app.services.laravel_client import LaravelClient
from app.services.vectorstore import VectorStoreService
from app.core.config import settings

def main():
    laravel = LaravelClient()
    vectorstore = VectorStoreService()

    products = laravel.get_products(settings.LARAVEL_API_TOKEN)

    if not isinstance(products, list):
        raise Exception("Formato inesperado desde Laravel")

    print(f"📦 Productos recibidos: {len(products)}")

    vectorstore.build_index(products)

    print("✅ Índice FAISS generado correctamente")


if __name__ == "__main__":
    main()
