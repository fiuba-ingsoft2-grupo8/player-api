# Imports.
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from dotenv import load_dotenv
from resources.logger import logger, LOGGING_CONFIG
import uvicorn
import controllers.player_controller as player_controller

# Load environment variables and configurations.
logger.info("Load configurations")
load_dotenv()

# FastAPI application setup.
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Initialize FastAPI app.
logger.info("Initializing FastAPI application")
app = FastAPI(title="Player API", version="1.0.0")
logger.info("FastAPI application initialized")

# CORS Middleware configuration.
allowed = [o.strip() for o in settings.allowed_origins.split(",")] if settings.allowed_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed if allowed != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers.
app.include_router(player_controller.router, prefix="/player", tags=["player"])

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return JSONResponse(status_code=200, content={})

# Run the application.
if __name__ == "__main__":
    logger.info("Starting Fast API")
    uvicorn.run(app, host=HOST, port=PORT, log_config=LOGGING_CONFIG)
