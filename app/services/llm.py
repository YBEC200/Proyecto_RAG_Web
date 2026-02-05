from openai import OpenAI
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    SYSTEM_PROMPT = """
        Eres un asistente especializado EXCLUSIVAMENTE en hardware para computadoras
        de la empresa Corporación CDT.

        REGLAS OBLIGATORIAS:
        - Usa ÚNICAMENTE la información proporcionada en el contexto.
        - NO inventes precios, stock ni características.
        - Si la información no es suficiente, responde claramente que no hay datos.
        - NO respondas preguntas fuera del ámbito de hardware.
        - NO asumas compatibilidades no explícitas.

        INFORMACIÓN CORPORATIVA (siempre visible):
        - Ubicación: Jirón Giráldez
        - Horario: 8:00 AM a 10:00 PM
        - Contacto: Ing. Carlos Yépez | 933 455 454 | CDT@gmail.com

        FORMATO DE RESPUESTA:
        1. Respuesta clara y directa
        2. Detalle técnico (si aplica)
        3. Invitación a contacto o compra
        """

    def generate_response(
        self,
        question: str,
        products: list[dict]
    ) -> str:
        if not products:
            return (
                "No encontré productos disponibles relacionados con tu consulta. "
                "Puedes visitarnos en Jirón Giráldez para recibir asesoría personalizada."
            )

        context = self._build_context(products)

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"""
                        PREGUNTA:
                        {question}

                        CONTEXTO DISPONIBLE (usar exclusivamente):
                        {context}
                        """
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    def _build_context(self, products: list[dict]) -> str:
        """
        Contexto estructurado y estable.
        Preparado para embeddings en el siguiente paso.
        """
        lines = []

        for p in products:
            lines.append(
                f"""
Producto:
- Nombre: {p.get('nombre')}
- Marca: {p.get('marca')}
- Precio: {p.get('precio', 'No disponible')}
- Stock: {p.get('stock', 'No disponible')}
"""
            )

        return "\n".join(lines)
