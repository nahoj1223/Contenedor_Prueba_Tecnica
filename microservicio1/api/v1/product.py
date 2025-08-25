from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from domain.use_cases.create_product import CreateProduct
from domain.use_cases.get_product import GetProduct
from domain.use_cases.list_products import ListProducts
from domain.use_cases.put_product import UpdateProduct
from domain.use_cases.delete_product import DeleteProduct
from infrastructure.db.database import get_db
from infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from schemas.product_schema import *
from utils.responses import common_responses
from core.logger import logger

router = APIRouter()
repo = ProductRepositoryImpl()

#CREATE PRODUCTS
@router.post("/products", response_model=ProductResponseMessage, responses=common_responses, summary="Create a new product")
def create_product(product: Product, db: Session = Depends(get_db)):
    use_case = CreateProduct(repo)
    try:
        created = use_case.execute(db, product)
        logger.info(f"🟢 Product created: {created.sku}")
        return {
            "message": "Product created", 
            "product": Product(**product.__dict__)
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un producto con ese SKU."
        )
    except Exception as e:
        logger.error(f"🚨 Error creating product: {e}")
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )

#LIST PRODUCTS
@router.get("/products/list", response_model=ProductResponseList, responses=common_responses, summary="List all products")
def list_products(db: Session = Depends(get_db)):
    use_case = ListProducts(repo)
    try:
        products = use_case.execute(db)
        if not products:
            raise HTTPException(status_code=404, detail="No hay productos")
        
        logger.info(f"🟢 Products returned: {len(products)}")
        return {
            "cuantity": len(products),
            "products": [Product(**product.__dict__) for product in products]
        }
    
    except Exception as e:
        logger.error(f"🚨 Error listing products: {e}")
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )

#GET PRODUCT BY SKU
@router.get("/products/{sku}", response_model=Product, responses=common_responses, summary="Search product by sku")
def get_product(sku: str, db: Session = Depends(get_db)):
    use_case = GetProduct(repo)
    try:
        product = use_case.execute(db, sku)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        logger.info(f"🟢 Product returned: {sku}")
        return Product(**product.__dict__)
    except Exception as e:
        logger.error(f"🚨 Error getting products: {e}")
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )
    
#UPDATE PRODUCTS
@router.put("/products/{sku}", response_model=ProductResponseMessage,responses=common_responses, summary="Update product")
def create_product(sku: str, product: ProductUpdate, db: Session = Depends(get_db)):
    use_case = UpdateProduct(repo)
    try:
        if product.name is None and product.base_price is None and product.currency is None and product.category is None:
            raise HTTPException(status_code=400, detail="No se ha proporcionado ningun campo para actualizar")

        updated = use_case.execute(db, sku, product)

        if updated.sku is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        logger.info(f"⚠️ Product updated: {sku}")
        return {
            "message": "Product updated", 
            "product": Product(**updated.__dict__)
        }
    except Exception as e:
        logger.error(f"🚨 Error updating product: {e}")
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )
    
#DELETE PRODUCTS
@router.delete("/products/{sku}", status_code=status.HTTP_204_NO_CONTENT,responses=common_responses, summary="Delete product")  
def delete_product(sku: str, db: Session = Depends(get_db)):
    use_case = DeleteProduct(repo)
    try:
        deleted = use_case.execute(db, sku)

        if not deleted:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        logger.info(f"⚠️ Product deleted: {sku}")
        return
    except Exception as e:
        logger.error(f"🚨 Error deleting product: {e}")
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )