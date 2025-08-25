from typing import Optional
from pydantic import BaseModel, Field

class Country(BaseModel):
    code: str
    name: str
    iva: float = Field(gt=0)

class CountryUpdate(BaseModel):
    name: Optional[str] = None
    iva: Optional[float] = Field(default=None, gt=0)

class CountryResponseMessage(BaseModel):
    message: str
    country: Country

class CountryResponseList(BaseModel):
    cuantity: int
    countries: list[Country]

class ErrorResponse(BaseModel):
    detail: str