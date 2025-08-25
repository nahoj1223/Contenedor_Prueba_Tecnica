from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class CurrencyEnum(str, Enum):
    COP = "COP"
    USD = "USD"

class Product(BaseModel):
    sku: str
    name: str
    base_price: int = Field(gt=0)
    currency: CurrencyEnum
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    base_price: Optional[int] = Field(default=None, gt=0)
    currency: Optional[CurrencyEnum] = None
    category: Optional[str] = None

class ProductResponseMessage(BaseModel):
    message: str
    product: Product

class ProductResponseList(BaseModel):
    cuantity: int
    products: list[Product]

class ErrorResponse(BaseModel):
    detail: str