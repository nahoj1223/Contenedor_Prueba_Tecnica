from domain.entities.country import Country
from domain.repositories.country_repository import CountryRepository
from sqlalchemy.orm import Session

class GetCountry:
    def __init__(self, repository: CountryRepository):
        self.repository = repository

    def execute(self, db: Session, code: str) -> Country:
        return self.repository.get(db, code)
