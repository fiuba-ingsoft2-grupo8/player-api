from fastapi import APIRouter
import schemas as s
from resources.logger import logger

router = APIRouter()

@router.get("/", response_model=s.Health)
def health():
    logger.info("Health check")
    return {"status": "ok"}