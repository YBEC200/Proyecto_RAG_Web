import requests
from app.core.config import settings

class LaravelClient:
    def __init__(self):
        self.base_url = settings.LARAVEL_API_BASE

    def get_products(self, token: str):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = requests.get(
            f"{self.base_url}/chat/productos",
            headers=headers
        )

        print("DEBUG STATUS:", response.status_code)
        print("DEBUG RESPONSE:", response.text)

        response.raise_for_status()
        return response.json()
    
    def get_stock_by_ids(self, token: str, ids: list[int]):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = requests.post(
            f"{self.base_url}/chat/productos-stock",
            json={"ids": ids},
            headers=headers
        )

        response.raise_for_status()
        return response.json()
