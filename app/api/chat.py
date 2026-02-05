from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.services.intent import IntentClassifier
from app.services.llm import LLMService
from app.services.vectorstore import VectorStoreService

router = APIRouter(prefix="/chat", tags=["chat"])

classifier = IntentClassifier()
llm = LLMService()
vectorstore = VectorStoreService()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(
    req: ChatRequest,
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")

    intent = classifier.classify(req.message)

    products = vectorstore.search(req.message)

    if not products:
        return {
            "intent": intent,
            "answer": "No encontré productos relacionados con tu consulta."
        }

    answer = llm.generate_response(
        message=req.message,
        intent=intent,
        products=products
    )

    return {
        "intent": intent,
        "answer": answer
    }
