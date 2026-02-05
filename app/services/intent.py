import re
import unicodedata

class IntentClassifier:
    def normalize_text(self, text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        return text
    
    def classify(self, message: str) -> str:
        text = self.normalize_text(message)

        intents = {
            "precio": ["precio", "cuesta", "vale", "costo"],
            "stock": ["stock", "hay", "disponible", "existencias"],
            "caracteristicas": ["características", "especificaciones", "velocidad", "capacidad"],
            "compatibilidad": ["compatible", "funciona", "sirve", "soporta"],
        }

        for intent, keywords in intents.items():
            for kw in keywords:
                if re.search(rf"\b{kw}\b", text):
                    return intent

        return "general"
