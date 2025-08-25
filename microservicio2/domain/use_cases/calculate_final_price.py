from domain.entities.pricing import Pricing
from domain.repositories.pricing_repository import PricingRepository
from schemas.pricing_schema import PricingResponse
from sqlalchemy.orm import Session

class CalculateFinalPrice:
    def __init__(self, repository: PricingRepository):
        self.repository = repository

    def execute(self, db: Session, pricing: Pricing) -> PricingResponse:
        return self.repository.calculate_final_price(db, pricing)
