from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.health import router as health_router
from api.v1.pricing import router as pricing_router
from core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔄 Iniciando aplicación...")
    yield
    logger.info("⚠️ Cerrando aplicación...")

app = FastAPI(
    title="🛍️ API - Microservice Pricing",
    description="API for pricing management.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(pricing_router, tags=["Pricing"])
app.include_router(health_router, tags=["Health"])
