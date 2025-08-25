from sqlalchemy import Column, String, Integer
from infrastructure.db.database import Base

class ProductModel(Base):
    __tablename__ = "products"

    sku = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_price = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    category = Column(String, nullable=False)