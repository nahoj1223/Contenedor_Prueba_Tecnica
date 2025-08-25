from domain.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class ListProducts:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, db: Session) -> list:
        return self.repository.list(db)