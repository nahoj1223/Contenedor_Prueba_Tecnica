from dataclasses import dataclass
from datetime import datetime

@dataclass
class Coupon:
    code: str
    description: str
    discount_percentage: float
    valid_from: datetime
    valid_to: datetime
    is_active: bool