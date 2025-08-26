from domain.entities.pricing import Pricing
from infrastructure.repositories.pricing_repository_api import PricingRepositoryAPI

class CheckFinalPriceUseCase:
    def __init__(self, repository: PricingRepositoryAPI):
        self.repository = repository

    def execute(self, pricing: Pricing):
        return self.repository.check_final_price(pricing)