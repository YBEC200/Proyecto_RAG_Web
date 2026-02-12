from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["chat"])

rag_service = RAGService()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(
    req: ChatRequest,
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")

    answer = rag_service.ask(
        question=req.message,
        token=authorization.replace("Bearer ", "")
    )

    return {
        "answer": answer
    }

