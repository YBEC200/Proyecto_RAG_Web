import requests
from app.core.config import settings


class LaravelClient:
    def __init__(self):
        self.base_url = settings.LARAVEL_API_BASE

    def get_products(self, token: str) -> list[dict]:
        headers = {
            "Authorization": token,  # Bearer ya viene incluido
            "Accept": "application/json"
        }

        response = requests.get(
            f"{self.base_url}/chat/productos",
            headers=headers,
            timeout=5
        )

        if response.status_code != 200:
            raise Exception(
                f"Error backend Laravel: {response.status_code}"
            )

        return response.json()
