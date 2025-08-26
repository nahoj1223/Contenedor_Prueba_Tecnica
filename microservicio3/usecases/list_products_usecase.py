from infrastructure.repositories.product_repository_api import ProductRepositoryAPI

class ListProductsUseCase:
    def __init__(self, repository: ProductRepositoryAPI):
        self.repository = repository

    def execute(self) -> list | None:
        return self.repository.list_product()