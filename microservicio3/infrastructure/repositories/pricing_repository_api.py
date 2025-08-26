import requests
from domain.entities.pricing import Pricing

class PricingRepositoryAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def check_final_price(self, pricing: Pricing):
        payload = {
            "sku": pricing.sku,
            "country": pricing.country,
            "coupon": pricing.coupon
        }
        response = requests.post(f"{self.base_url}/pricing/quote", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error consultando el precio final del producto: {response.text}")
    