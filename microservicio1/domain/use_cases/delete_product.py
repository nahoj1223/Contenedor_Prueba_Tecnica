from domain.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class DeleteProduct:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, db: Session, sku: str)  -> bool:
        return self.repository.delete(db, sku)
