from abc import ABC, abstractmethod
from domain.entities.pricing import Pricing
from schemas.pricing_schema import PricingResponse
from sqlalchemy.orm import Session

class PricingRepository(ABC):

    @abstractmethod
    def calculate_final_price(self, db: Session, pricing: Pricing) -> PricingResponse:
        pass