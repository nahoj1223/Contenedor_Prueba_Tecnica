from domain.entities.coupon import Coupon
from domain.repositories.coupon_repository import CouponRepository
from infrastructure.db.coupon_model import CouponModel
from infrastructure.mappers.coupon_mapper import *
from sqlalchemy.orm import Session

class CouponRepositoryImpl(CouponRepository):

    def get(self, db: Session, code: str) -> Coupon:
        db_coupon = db.query(CouponModel).filter_by(code=code).first()
        return map_model_to_entity(db_coupon) if db_coupon else None