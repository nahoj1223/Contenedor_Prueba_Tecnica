from domain.entities.product import Product
from schemas.product_schema import ProductUpdate
from domain.repositories.product_repository import ProductRepository
from infrastructure.db.product_model import ProductModel
from infrastructure.mappers.product_mapper import *
from sqlalchemy.orm import Session

class ProductRepositoryImpl(ProductRepository):

    def save(self, db: Session, product: Product):
        db_product = ProductModel(**product.__dict__)
        db.add(db_product)
        db.commit()

    def get(self, db: Session, sku: str) -> Product:
        db_product = db.query(ProductModel).filter_by(sku=sku).first()
        return map_model_to_entity(db_product) if db_product else None

    def list(self, db: Session) -> list:
        db_product = db.query(ProductModel).all()
        return map_model_to_entity_list(db_product) if db_product else None
    
    def update(self, db: Session, sku: str, product: ProductUpdate):

        db_product = db.query(ProductModel).filter_by(sku=sku).first()

        if not isinstance(db_product, ProductModel):
            return db_product
        
        db_product.name = product.name if product.name is not None else db_product.name
        db_product.base_price = product.base_price if product.base_price is not None else db_product.base_price
        db_product.currency = product.currency if product.currency is not None else db_product.currency
        db_product.category = product.category if product.category is not None else db_product.category

        db.commit()
        db.refresh(db_product)

        return db_product
    
    def delete(self, db: Session, sku: str) -> bool:
        product = db.query(ProductModel).filter_by(sku=sku).first()

        if not product:
            return False

        db.delete(product)
        db.commit()
        return True