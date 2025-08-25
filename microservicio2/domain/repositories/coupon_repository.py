from abc import ABC, abstractmethod
from domain.entities.coupon import Coupon
from sqlalchemy.orm import Session

class CouponRepository(ABC):

    @abstractmethod
    def get(self, db: Session, code: str) -> Coupon:
        pass