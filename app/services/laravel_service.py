from app.services.laravel_client import LaravelClient
from app.services.vectorstore import VectorStoreService
from app.services.intent import IntentClassifier
from app.core.config import settings
from app.services.llm_service import LLMService


class LaravelService:

    def __init__(self):
        self.client = LaravelClient()
        self.vectorstore = VectorStoreService()
        self.intent_classifier = IntentClassifier()
        self.llm = LLMService()  # 👈 agregado

    def ask(self, question: str, token: str = None) -> str:
        if not token:
            token = settings.LARAVEL_API_TOKEN

        normalized = self.intent_classifier.normalize_text(question)

        # 🔹 Empresa
        if any(word in normalized for word in ["empresa", "ubicacion", "direccion", "horario", "contacto"]):
            return self._handle_empresa()
        
        # 🔹 1️⃣ Obtener todos los productos
        products = self.client.get_products(token)

        if not products:
            return "No se pudieron obtener productos."

        # 🔹 2️⃣ Reconstruir índice en memoria
        self.vectorstore.build_index_if_needed(products)

        # 🔹 Buscar productos en FAISS
        docs = self.vectorstore.search(question, k=3)

        if not docs:
            return "No pude identificar el producto al que te refieres."

        product_ids = [doc.metadata.get("id") for doc in docs if doc.metadata.get("id")]

        if not product_ids:
            return "No pude obtener el identificador del producto."

        # 🔹 Consultar datos reales
        stock_data = self.client.get_stock_by_ids(token, product_ids)

        if not stock_data:
            return "No se pudo obtener información en este momento."

        # 🔹 Construimos contexto REAL
        data_context = ""
        for item in stock_data:
            data_context += (
                f"Producto: {item.get('nombre')}\n"
                f"Marca: {item.get('marca')}\n"
                f"Precio: {item.get('precio')}\n"
                f"Stock disponible: {item.get('stock_total')}\n\n"
            )

        # 🔥 Ahora usamos IA para redactar
        prompt = f"""
        Eres un asistente de ventas experto en hardware.

        DATOS REALES DEL SISTEMA:
        {data_context}

        INSTRUCCIONES OBLIGATORIAS:
        - Usa EXCLUSIVAMENTE la información contenida en los datos reales.
        - No agregues especificaciones técnicas que no aparezcan en los datos.
        - No supongas generación, rendimiento ni compatibilidad si no está explícitamente indicado.
        - Si la información es insuficiente, indica que no hay más detalles registrados.

        Responde de manera natural y profesional.

        Pregunta del cliente:
        {question}
        """

        return self.llm.ask(prompt)

    # ==========================
    # Empresa
    # ==========================
    def _handle_empresa(self) -> str:
        return (
            "📍 Corporación CDT\n"
            "Ubicación: Jirón Giráldez\n"
            "Horario: 8:00 AM a 10:00 PM\n"
            "Contacto: Ing. Carlos Yépez | 933 455 454 | CDT@gmail.com"
        )
