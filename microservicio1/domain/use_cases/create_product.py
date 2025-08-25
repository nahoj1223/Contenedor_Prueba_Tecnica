from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class CreateProduct:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, db: Session, product: Product) -> Product:
        self.repository.save(db, product)
        return product