from dataclasses import dataclass

@dataclass
class Product:
    sku: str
    name: str
    base_price: int
    currency: str
    category: str