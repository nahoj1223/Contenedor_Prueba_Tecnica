from schemas.pricing_schema import PricingResponse
from domain.entities.pricing import Pricing
from domain.repositories.pricing_repository import PricingRepository
from sqlalchemy.orm import Session
from infrastructure.repositories.country_repository_impl import CountryRepositoryImpl
from infrastructure.repositories.coupon_repository_impl import CouponRepositoryImpl
from domain.use_cases.get_country import GetCountry
from domain.use_cases.get_coupon import GetCoupon
from domain.external_services.product_api_client import ProductAPIClient
from core.logger import logger
from datetime import date

class PricingRepositoryImpl(PricingRepository):
    def __init__(self, product_api: ProductAPIClient, repoCountry: CountryRepositoryImpl, repoCoupon: CouponRepositoryImpl):
        self.product_api = product_api
        self.repoCountry = repoCountry
        self.repoCoupon = repoCoupon

    def calculate_final_price(self, db: Session, pricing: Pricing) -> PricingResponse:

        response = PricingResponse()

        #Insantciamos los casos de uso
        use_case_country = GetCountry(self.repoCountry)
        use_case_coupon = GetCoupon(self.repoCoupon)

        #Consultamos el iva del pais y el descuento del cupon
        coupon = use_case_coupon.execute(db, pricing.coupon)
        country = use_case_country.execute(db, pricing.country)

        #Validamos si se encontro el pais
        if country is None:
            response.is_valid_country = False
            return response
        
        response.is_valid_country = True
        response.iva = country.iva 

        #Establecemos los valores del cupon
        if coupon is None:
            response.is_valid_coupon = False
            response.discount_coupon = 0.0
        else:
            if not coupon.is_active:
                response.is_valid_coupon = False
                response.discount_coupon = 0.0
            else:
                hoy = date.today()
                if coupon.valid_from <= hoy <= coupon.valid_to:
                    response.is_valid_coupon = True
                    response.discount_coupon = coupon.discount_percentage
                else:
                    response.is_valid_coupon = False
                    response.discount_coupon = 0.0

        #Consultamos el producto en la API externa
        product_data = self.product_api.get_product(pricing.sku)

        #Validamos si se encontro el producto
        if 'name' not in product_data:
            response.product_name = None
            logger.info(f"{str(product_data)}")
            return response
        
        #Diligenciamos los datos faltantes de la respuesta
        response.sku = pricing.sku
        response.product_name = product_data['name']
        response.base_price = product_data['base_price']
        response.coupon = pricing.coupon

        #Calculamos el precio final
        precio_descuento = product_data['base_price'] * (1 - (response.discount_coupon/100))
        iva = precio_descuento * (response.iva /100)

        #Asignamos el precio final
        response.final_price =  precio_descuento + iva

        return response