from typing import Optional
from pydantic import BaseModel, Field

class Pricing(BaseModel):
    sku: str
    country: str
    coupon: str

class PricingResponse(BaseModel):
    sku: Optional[str] = None
    product_name: Optional[str] = None
    base_price: Optional[float] = 0.0
    iva: Optional[float] = 0.0
    is_valid_country: Optional[bool] = None
    coupon: Optional[str] = None
    is_valid_coupon: Optional[bool] = False
    discount_coupon: Optional[float] = 0.0
    final_price: Optional[float] = False

class ErrorResponse(BaseModel):
    detail: str