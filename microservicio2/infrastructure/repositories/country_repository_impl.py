from domain.entities.country import Country
from domain.repositories.country_repository import CountryRepository
from infrastructure.db.country_model import CountryModel
from infrastructure.mappers.country_mapper import *
from sqlalchemy.orm import Session

class CountryRepositoryImpl(CountryRepository):

    def get(self, db: Session, code: str) -> Country:
        db_country = db.query(CountryModel).filter_by(code=code).first()
        return map_model_to_entity(db_country) if db_country else None