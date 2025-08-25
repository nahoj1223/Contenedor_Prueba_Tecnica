from domain.entities.product import Product
from schemas.product_schema import ProductUpdate
from domain.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class UpdateProduct:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, db: Session, sku: str, product: ProductUpdate) -> Product:
        return self.repository.update(db, sku, product)