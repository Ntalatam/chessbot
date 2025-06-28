from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Text, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..db.base import Base

# Enums for type safety
class GameResult(str, Enum):
    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"
    DRAW = "1/2-1/2"
    UNFINISHED = "*"

class PuzzleDifficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    elo_rating = Column(Integer, default=1200)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    games = relationship("Game", back_populates="user")
    puzzle_sessions = relationship("PuzzleSession", back_populates="user")
    coaching_sessions = relationship("CoachingSession", back_populates="user")
    analyses = relationship("Analysis", back_populates="user")

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pgn = Column(Text)
    result = Column(String)
    time_control = Column(String)
    date_played = Column(DateTime, default=datetime.utcnow)
    analysis = Column(JSON)
    
    user = relationship("User", back_populates="games")

class PuzzleSession(Base):
    __tablename__ = "puzzle_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    puzzle_fen = Column(String)
    solution = Column(JSON)
    user_solution = Column(JSON)
    is_correct = Column(Boolean)
    time_taken = Column(Float)
    difficulty = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="puzzle_sessions")

class Analysis(Base):
    """Stores analysis results for chess positions"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    fen = Column(String, nullable=False, index=True)
    depth = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    evaluation = Column(JSON)  # Stores centipawn evaluation and mate info
    best_move = Column(String)  # UCI format
    pv = Column(JSON)  # Principal variation
    top_moves = Column(JSON)  # List of top moves with evaluations
    analysis_data = Column(JSON)  # Raw analysis data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    
    class Config:
        orm_mode = True


class AnalysisCreate(BaseModel):
    """Pydantic model for creating a new analysis"""
    fen: str
    depth: int
    evaluation: Optional[Dict[str, Any]] = None
    best_move: Optional[str] = None
    pv: Optional[List[str]] = None
    top_moves: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "depth": 18,
                "best_move": "e2e4",
                "evaluation": {"value": 0.2, "type": "cp"}
            }
        }


class CoachingSession(Base):
    __tablename__ = "coaching_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fen = Column(String)
    pgn = Column(Text)
    analysis = Column(JSON)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="coaching_sessions")
