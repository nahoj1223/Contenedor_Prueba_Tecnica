from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class GetProduct:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, db: Session, sku: str) -> Product:
        return self.repository.get(db, sku)
