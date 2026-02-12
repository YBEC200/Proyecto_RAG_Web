"""
Test script para el RAG Chatbot
Precarga productos y prueba varios tipos de preguntas
"""
from app.services.rag_service import RAGService
from app.services.laravel_client import LaravelClient
from app.core.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 60)
print("🚀 INICIANDO TEST DEL RAG CHATBOT")
print("=" * 60)

# 1️⃣ Crear instancia de RAG
rag = RAGService()
logger.info("✅ Instancia de RAG creada")

# 2️⃣ Precarga productos (como hace main.py en startup)
try:
    logger.info("🔄 Cargando productos desde Laravel...")
    laravel = LaravelClient()
    products = laravel.get_products(settings.LARAVEL_API_TOKEN)
    logger.info(f"✅ {len(products)} productos cargados")
    
    # Construir índice
    rag.vectorstore.build_index_if_needed(products)
    logger.info("✅ Índice FAISS construido")
except Exception as e:
    logger.error(f"❌ Error precargando productos: {e}")
    exit(1)

# 3️⃣ Pruebas
tests = [
    "¿Quién eres?",
    "¿Qué tarjetas gráficas tienen disponible?",
    "¿Cuál es el monitor más recomendado?",
    "¿Dónde están ubicados?",
    "¿Cuál es el horario de atención?",
]

print("\n" + "=" * 60)
print("📝 EJECUTANDO TESTS")
print("=" * 60)

for i, question in enumerate(tests, 1):
    print(f"\n[Test {i}/{len(tests)}]")
    print(f"❓ Pregunta: {question}")
    print("-" * 60)
    
    try:
        response = rag.ask(question)
        print(f"🤖 Respuesta: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

print("=" * 60)
print("✅ TESTS COMPLETADOS")
print("=" * 60)

