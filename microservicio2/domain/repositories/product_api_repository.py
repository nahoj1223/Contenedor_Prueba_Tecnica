from abc import ABC, abstractmethod

class ProductAPIRepository(ABC):
    @abstractmethod
    def get_product(self, sku: str) -> dict:
        pass