from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Coupon(BaseModel):
    code: str
    description: str
    discount_percentage: float = Field(gt=0)
    valid_from: datetime
    valid_to: datetime
    is_active: bool

class CouponUpdate(BaseModel):
    description: Optional[str] = None
    discount_percentage: Optional[float] = Field(default=None, gt=0)
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    is_active: Optional[bool] = None

class CouponResponseMessage(BaseModel):
    message: str
    coupon: Coupon

class CouponResponseList(BaseModel):
    cuantity: int
    coupons: list[Coupon]

class ErrorResponse(BaseModel):
    detail: str