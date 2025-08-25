from sqlalchemy import Column, String, Integer, Date, Boolean
from infrastructure.db.database import Base

class CouponModel(Base):
    __tablename__ = "coupons"

    code = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False)