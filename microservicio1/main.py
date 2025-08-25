from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.health import router as health_router
from api.v1.product import router as product_router
from core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔄 Iniciando aplicación...")
    yield
    logger.info("⚠️ Cerrando aplicación...")

app = FastAPI(
    title="🛍️ API - Microservice Products",
    description="API for product management.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(product_router, tags=["Product"])
app.include_router(health_router, tags=["Health"])
