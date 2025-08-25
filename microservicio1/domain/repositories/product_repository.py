from abc import ABC, abstractmethod
from domain.entities.product import Product
from schemas.product_schema import ProductUpdate
from sqlalchemy.orm import Session

class ProductRepository(ABC):
    @abstractmethod
    def save(self, db: Session, product: Product):
        pass

    @abstractmethod
    def get(self, db: Session, sku: str) -> Product:
        pass

    @abstractmethod
    def list(self, db: Session) -> list:
        pass

    @abstractmethod
    def update(self, db: Session, sku: str, product: ProductUpdate) -> Product:
        pass

    @abstractmethod
    def delete(self, db: Session, sku: str)  -> bool:
        pass