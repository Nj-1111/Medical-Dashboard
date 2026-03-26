"""
FastAPI Application Entry Point
Medical Diagnosis Pipeline
"""
import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api import routes
from app.utils.logging_config import setup_logging

# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Glaucoma Model: {settings.GLAUCOMA_MODEL_NAME}")
    logger.info(f"LLM Model: {settings.LLM_MODEL_NAME}")
    
    # Load models if configured
    if settings.LOAD_MODELS_ON_STARTUP:
        logger.info("Loading ML models...")
        try:
            from app.ml.inference import InferenceEngine
            InferenceEngine.initialize()
            logger.info("✓ ML models loaded successfully")
        except Exception as e:
            logger.error(f"✗ Failed to load ML models: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade medical diagnosis pipeline with glaucoma detection",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {process_time:.3f}s"
    )
    
    return response


# Include routes
app.include_router(routes.auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(routes.patient_router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(routes.upload_router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(routes.inference_router, prefix="/api/v1/inference", tags=["Inference"])
app.include_router(routes.health_router, prefix="/api/v1/health", tags=["Health"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "documentation": "/docs"
    }


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
