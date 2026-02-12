from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router, set_rag_service
from app.services.rag_service import RAGService
from app.services.laravel_client import LaravelClient
from app.services.vectorstore import VectorStoreService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
app = FastAPI(title="Chat IA")

# ============================================
# CORS Middleware
# ============================================
allowed_origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Instancia global de RAGService
# ============================================
rag_service = RAGService()


@app.on_event("startup")
async def startup_event():
    """
    Precarga productos al iniciar.
    Evita regenerar índice en cada petición (mejora rendimiento).
    """
    global rag_service
    
    try:
        logger.info("🔄 Cargando productos desde Laravel...")
        laravel = LaravelClient()
        
        products = laravel.get_products(settings.LARAVEL_API_TOKEN)
        logger.info(f"✅ {len(products)} productos cargados")
        
        # Construir índice (método correcto)
        rag_service.vectorstore.build_index_if_needed(products)
        logger.info("✅ Índice FAISS construido exitosamente")
        
        # Inyectar instancia en chat.py
        set_rag_service(rag_service)
        logger.info("✅ RAG Service inyectado en router")
        
    except Exception as e:
        logger.error(f"❌ Error precargando productos: {e}")
        # Continúa aunque falle, RAG puede intentar manualmente después


app.include_router(chat_router)
