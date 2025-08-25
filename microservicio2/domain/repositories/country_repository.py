from abc import ABC, abstractmethod
from domain.entities.country import Country
from sqlalchemy.orm import Session

class CountryRepository(ABC):

    @abstractmethod
    def get(self, db: Session, code: str) -> Country:
        pass