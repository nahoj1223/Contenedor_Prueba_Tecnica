from sqlalchemy import Column, String, Integer
from infrastructure.db.database import Base

class CountryModel(Base):
    __tablename__ = "countries"

    code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    iva = Column(Integer, nullable=False)