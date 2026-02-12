from app.services.vectorstore import VectorStoreService
from app.services.llm_service import LLMService
from app.services.intent import IntentClassifier
from app.services.laravel_service import LaravelService  # 👈 nuevo


BASE_PROMPT = """
Eres un asistente especializado en hardware para computadoras
de la empresa Corporación CDT (las siglas son abreviacion de Corporacion Digital Technology).

INFORMACIÓN CORPORATIVA:
- Ubicación: Jirón Giráldez
- Horario: 8:00 AM a 10:00 PM
- Contacto: Ing. Carlos Yépez | 933 455 454 | CDT@gmail.com

FORMATO:
1. Respuesta clara
2. Explicación técnica
3. Invitación a contacto o compra
"""


class RAGService:

    def __init__(self):
        self.vectorstore = VectorStoreService()
        self.llm = LLMService()
        self.intent_classifier = IntentClassifier()
        self.laravel_service = LaravelService()  # 👈 nuevo

    def ask(self, question: str, token: str) -> str:
        intent = self.intent_classifier.classify(question)

        if intent == "compatibilidad":
            return self.handle_compatibilidad(question)

        elif intent == "datos":
            return self.handle_datos(question, token)

        else:
            return self.handle_general(question)

    # ==========================
    # DATOS → Laravel
    # ==========================
    def handle_datos(self, question: str, token: str) -> str:
        """
        Aquí NO se usa vectorstore.
        Solo se consulta Laravel.
        """
        return self.laravel_service.ask(question, token)

    # ==========================
    # COMPATIBILIDAD → RAG + LLM
    # ==========================
    def handle_compatibilidad(self, question: str) -> str:
        docs = self.vectorstore.search(question, k=5)

        if not docs:
            return "No encontré productos relacionados para analizar compatibilidad."

        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
{BASE_PROMPT}

Eres experto en compatibilidad de hardware.

INSTRUCCIONES ESPECÍFICAS:
- Puedes usar conocimiento técnico general sobre hardware.
- Analiza la compatibilidad basada en socket, generación, chipset o tipo de tecnología.
- SOLO recomienda productos que aparezcan en el contexto, osea en la empresa.
- No inventes productos que no estén listados.

Productos disponibles en tienda:
{context}

Pregunta del cliente:
{question}
"""

        return self.llm.ask(prompt)

    # ==========================
    # GENERAL → RAG normal
    # ==========================
    def handle_general(self, question: str) -> str:
        

        docs = self.vectorstore.search(question, k=3)

        if not docs:
            return "No encontré productos relacionados."

        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
{BASE_PROMPT}

REGLAS:
- Usa únicamente la información proporcionada en el contexto.
- No inventes especificaciones.
- No inventes stock ni precios.

Productos:
{context}

Pregunta:
{question}
"""

        return self.llm.ask(prompt)
