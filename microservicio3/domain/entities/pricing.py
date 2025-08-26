from dataclasses import dataclass

@dataclass
class Pricing:
    sku: str
    country: str
    coupon: str