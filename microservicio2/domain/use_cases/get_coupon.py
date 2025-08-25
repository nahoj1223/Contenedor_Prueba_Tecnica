from domain.entities.coupon import Coupon
from domain.repositories.coupon_repository import CouponRepository
from sqlalchemy.orm import Session

class GetCoupon:
    def __init__(self, repository: CouponRepository):
        self.repository = repository

    def execute(self, db: Session, code: str) -> Coupon:
        return self.repository.get(db, code)
