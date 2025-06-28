from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import random

from .. import models
from ..db.session import get_db

router = APIRouter()

class PuzzleRequest(BaseModel):
    difficulty: Optional[str] = None
    themes: Optional[List[str]] = None
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None

class PuzzleResponse(BaseModel):
    id: int
    fen: str
    moves: List[str]
    rating: int
    themes: List[str]
    difficulty: str



@router.post("/get", response_model=PuzzleResponse)
def get_puzzle(
    request: PuzzleRequest,
    db: Session = Depends(get_db)
):
    """
    Get a puzzle based on difficulty, themes, and user's rating.
    """
    # Build query
    query = db.query(models.Puzzle)
    
    # Apply filters
    if request.difficulty:
        query = query.filter(models.Puzzle.difficulty == request.difficulty)
    
    if request.themes:
        # This is a simplified approach - in production, you'd want a proper many-to-many relationship
        query = query.filter(models.Puzzle.themes.contains(request.themes))
    
    if request.min_rating:
        query = query.filter(models.Puzzle.rating >= request.min_rating)
    
    if request.max_rating:
        query = query.filter(models.Puzzle.rating <= request.max_rating)
    
    # Get all matching puzzles
    puzzles = query.all()
    
    if not puzzles:
        raise HTTPException(status_code=404, detail="No puzzles found matching the criteria")
    
    # For now, return a random puzzle
    # In a real app, you might want to implement a more sophisticated selection algorithm
    puzzle = random.choice(puzzles)
    
    return {
        "id": puzzle.id,
        "fen": puzzle.fen,
        "moves": puzzle.moves,
        "rating": puzzle.rating,
        "themes": puzzle.themes,
        "difficulty": puzzle.difficulty
    }



@router.get("/themes", response_model=List[str])
def get_puzzle_themes():
    """
    Get a list of available puzzle themes.
    """
    # In a real app, you might want to get these from the database
    return [
        "checkmateInOne", "checkmateInTwo", "checkmateInThree",
        "fork", "pin", "skewer", "discovery", "deflection",
        "endgame", "middlegame", "opening",
        "kingsideAttack", "queensideAttack", "sacrifice",
        "advantage", "crushing", "onlyMove"
    ]


