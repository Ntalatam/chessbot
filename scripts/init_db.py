#!/usr/bin/env python3
"""
Initialize the database with required tables.
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import create_engine
from app.db.base import Base
from app.models.models import User, Game, GameAnalysis, Puzzle, PuzzleAttempt, TrainingSession
from app.core.config import settings

def init_db():
    """Initialize the database with all tables."""
    print("Initializing database...")
    
    # Create engine and connect to the database
    engine = create_engine(settings.DATABASE_URI)
    
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
