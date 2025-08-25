from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from domain.external_services.product_api_client import ProductAPIClient
from infrastructure.db.database import get_db
from domain.use_cases.calculate_final_price import CalculateFinalPrice
from infrastructure.repositories.country_repository_impl import CountryRepositoryImpl
from infrastructure.repositories.coupon_repository_impl import CouponRepositoryImpl
from infrastructure.repositories.pricing_repository_impl import PricingRepositoryImpl
from schemas.pricing_schema import *
from utils.responses import common_responses
from core.logger import logger

router = APIRouter()

repoCountry = CountryRepositoryImpl()
repoCoupon = CouponRepositoryImpl()
product_api = ProductAPIClient()

repo = PricingRepositoryImpl(product_api, repoCountry, repoCoupon)

#CREATE PRODUCTS
@router.post("/pricing/quote", response_model=PricingResponse, responses=common_responses, summary="Calculate final price to product", tags=["Pricing"])
def create_product(pricing: Pricing, db: Session = Depends(get_db)):

    use_case = CalculateFinalPrice(repo)
    try:
        response = use_case.execute(db, pricing)

        if not response.is_valid_country:
            raise HTTPException(
                status_code=400,
                detail="El codigo de pais ingresado no esta registrado en la tienda"
            )
        
        if response.product_name is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el producto ingresado."
            )
        
        logger.info(f"🟢 Final price calculated: {response.sku}")
        return response.__dict__

    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un producto con ese SKU."
        )
    except Exception as e:
        logger.error(f"🚨 Error calculating final price of product: {e}")
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )