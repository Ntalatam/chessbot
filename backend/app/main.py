from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .routers import analyze, coach, puzzles, dashboard, auth
from .core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Chess Coach API",
    description="API for the Chess Coach application, providing game analysis, coaching, and puzzle management.",
    version="1.0.0",
)



# Create database tables on startup
from .db.base import Base
from .db.session import engine

@app.on_event("startup")
def on_startup():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
app.include_router(coach.router, prefix="/api/coach", tags=["coach"])
app.include_router(puzzles.router, prefix="/api/puzzles", tags=["puzzles"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(auth.router, tags=["authentication"])

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {
        "message": "Welcome to Chess Coach API",
        "docs": "/docs",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
