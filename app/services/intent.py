import re
import unicodedata


class IntentClassifier:

    def normalize_text(self, text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize('NFD', text)
        text = ''.join(
            c for c in text if unicodedata.category(c) != 'Mn'
        )
        return text

    def classify(self, message: str) -> str:
        text = self.normalize_text(message)

        intents = {
            # 🔹 Datos reales (Laravel)
            "datos": [
                "precio", "cuesta", "vale", "costo",
                "stock", "hay", "disponible", "existencias",
                "empresa", "ubicacion", "direccion",
                "horario", "contacto", "telefono"
            ],

            # 🔹 Análisis técnico con IA
            "compatibilidad": [
                "compatible", "funciona", "sirve",
                "soporta", "socket", "chipset",
                "es compatible con"
            ],
        }

        for intent, keywords in intents.items():
            for kw in keywords:
                if re.search(rf"\b{kw}\b", text):
                    return intent

        # 🔹 Todo lo demás
        return "general"
