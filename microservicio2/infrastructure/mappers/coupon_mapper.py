from domain.entities.coupon import Coupon
from infrastructure.db.coupon_model import CouponModel

def map_model_to_entity(model: CouponModel) -> Coupon:
    return Coupon(
        code=model.code,
        description=model.description,
        discount_percentage=model.discount_percentage,
        valid_from=model.valid_from,
        valid_to=model.valid_to,
        is_active=model.is_active
    )

def map_model_to_entity_list(models: list[CouponModel]) -> list[Coupon]:
    return [map_model_to_entity(model) for model in models]
