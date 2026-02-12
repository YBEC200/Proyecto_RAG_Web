from app.services.rag_service import RAGService
from app.core.config import settings

rag = RAGService()

# Usa el mismo token que usas para indexar productos
token = settings.LARAVEL_API_TOKEN

tests = [
    "Quien eres?",
]

for question in tests:
    print("\n==============================")
    print("Pregunta:", question)
    print("------------------------------")
    response = rag.ask(question, token=token)
    print(response)
