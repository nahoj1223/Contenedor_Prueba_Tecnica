from fastapi import APIRouter
from sqlalchemy import text
from core.db import engine
from core.logger import logger

router = APIRouter()

@router.get("/health", summary="Comprobar estado de la api")
def health_check():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW();"))
            db_time = list(result)[0][0]
        logger.info("Health check OK")
        return {
            "status": "ok",
            "message": "Database connection successful",
            "time": db_time
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
