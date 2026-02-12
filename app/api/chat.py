from fastapi import APIRouter, Request
from pydantic import BaseModel, ValidationError
from app.services.rag_service import RAGService
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

# Instancia global (se inyecta desde main.py)
rag_service: RAGService = None


def set_rag_service(service: RAGService):
    """Inyecta la instancia de RAGService desde main.py"""
    global rag_service
    rag_service = service


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: Request):
    """
    Endpoint de chat directo para frontend.
    No requiere autenticación.
    """
    try:
        # Leer body directamente para debug
        body = await request.body()
        logger.info(f"Raw body: {body}")
        
        data = await request.json()
        logger.info(f"Parsed JSON: {data}")
        
        # Validar con Pydantic
        chat_req = ChatRequest(**data)
        
        if not rag_service:
            return {"answer": "❌ Servicio no inicializado"}
        
        logger.info(f"Processing question: {chat_req.message}")
        answer = rag_service.ask(question=chat_req.message)
        return {"answer": answer}
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {"answer": f"❌ Error de validación: {e}"}
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {"answer": f"❌ JSON inválido"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"answer": f"❌ Error: {str(e)}"}