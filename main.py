"""
WiFi Access Database - Main Entry Point
Handles application startup, initialization, and server launch
"""

import os
import sys
import logging
from typing import Generator
from contextlib import contextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Import database and API modules
from database import init_db, get_db, Base, engine
from api import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI application."""
    cors_origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:8000"]')
    
    # Parse CORS origins
    try:
        import json
        origins = json.loads(cors_origins)
    except (json.JSONDecodeError, TypeError):
        origins = ["http://localhost:3000", "http://localhost:8000"]
        logger.warning(f"Could not parse CORS_ORIGINS, using defaults: {origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS configured with origins: {origins}")


def initialize_database() -> None:
    """Initialize database tables and schema."""
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {e}")
        sys.exit(1)


def startup_event() -> None:
    """FastAPI startup event handler."""
    logger.info("=" * 60)
    logger.info("WiFi Access Monitoring System - Starting Up")
    logger.info("=" * 60)
    
    # Initialize database
    initialize_database()
    
    # Log environment info
    env = os.getenv("ENV", "development")
    app_name = os.getenv("APP_NAME", "WiFi Access Monitoring System")
    app_version = os.getenv("APP_VERSION", "1.0.0")
    
    logger.info(f"Environment: {env}")
    logger.info(f"Application: {app_name} v{app_version}")
    logger.info("=" * 60)


def shutdown_event() -> None:
    """FastAPI shutdown event handler."""
    logger.info("WiFi Access Monitoring System - Shutting Down")
    logger.info("Closing database connections...")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Setup CORS
    setup_cors(app)
    
    # Register startup and shutdown events
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)
    
    return app


# Create the application instance
application = create_application()


@application.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "WiFi Access Monitoring System is running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }


@application.get("/api/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check endpoint - verifies database connectivity."""
    try:
        # Attempt a simple query to verify database connection
        db.execute("SELECT 1")
        return {
            "status": "ready",
            "database": "connected",
            "message": "Application is ready to accept requests"
        }
    except Exception as e:
        logger.error(f"Database readiness check failed: {e}")
        return {
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e)
        }, 503


def main():
    """Main entry point for running the application."""
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:application",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
    )


if __name__ == "__main__":
    main()
