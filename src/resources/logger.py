"""
Logging configuration module for the Melodia API application.

This module sets up a centralized logging configuration using Python's logging
module. It configures formatters, handlers, and loggers to provide consistent
logging across the entire application.

The configuration includes:
- Default formatter with timestamp and log level
- Console handler for stdout output  
- Root logger configuration
- Specific uvicorn logger configurations

Environment variables:
- LOG_LEVEL: Sets the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  Defaults to INFO if not specified.
"""

# Imports.
import logging
import logging.config
import os

# Retrieve log level from environment variable, defaulting to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Define logging configuration dictionary
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["default"],
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# Apply logging configuration.
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
