from domain.entities.country import Country
from infrastructure.db.country_model import CountryModel

def map_model_to_entity(model: CountryModel) -> Country:
    return Country(
        code=model.code,
        name=model.name,
        iva=model.iva
    )

def map_model_to_entity_list(models: list[CountryModel]) -> list[Country]:
    return [map_model_to_entity(model) for model in models]
