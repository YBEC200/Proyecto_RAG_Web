from langchain_groq import ChatGroq
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model="llama-3.1-8b-instant",
            temperature=0.2
        )

    def ask(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
