import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from dotenv import load_dotenv
from resources.logger import logger, LOGGING_CONFIG
import uvicorn
import controllers.health_controller as health_controller
import controllers.tracks_controller as tracks_controller
import controllers.albums_controller as albums_controller
import controllers.artists_controller as artists_controller

logger.info("Load configurations")
load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

logger.info("Initializing FastAPI application")
app = FastAPI(title="Player API", version="1.0.0")
logger.info("FastAPI application initialized")

# CORS
allowed = [o.strip() for o in settings.allowed_origins.split(",")] if settings.allowed_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed if allowed != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_controller.router, prefix="/health", tags=["health"])
app.include_router(tracks_controller.router, prefix="/tracks", tags=["tracks"])
app.include_router(albums_controller.router, prefix="/albums", tags=["albums"])
app.include_router(artists_controller.router, prefix="/artists", tags=["artists"])

if __name__ == "__main__":
    logger.info("Starting Fast API")
    uvicorn.run(app, host=HOST, port=PORT, log_config=LOGGING_CONFIG)