from domain.entities.product import Product
from infrastructure.db.product_model import ProductModel

def map_model_to_entity(model: ProductModel) -> Product:
    return Product(
        sku=model.sku,
        name=model.name,
        base_price=model.base_price,
        currency=model.currency,
        category=model.category
    )

def map_model_to_entity_list(models: list[ProductModel]) -> list[Product]:
    return [map_model_to_entity(model) for model in models]
