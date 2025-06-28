from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from datetime import datetime, timedelta
from typing import List, Dict

# --- Functions for New Dashboard ---

def get_user_profile_data(db: Session, user_id: int) -> Dict:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {
            "username": "Guest",
            "elo": 1200,
            "games_played": 0,
            "record": {"wins": 0, "losses": 0, "draws": 0}
        }

    games_played = db.query(func.count(models.Game.id)).filter(models.Game.user_id == user_id).scalar() or 0
    
    # This logic needs to be more robust to check player color
    wins = db.query(func.count(models.Game.id)).filter(models.Game.user_id == user_id, models.Game.result == '1-0').scalar() or 0
    losses = db.query(func.count(models.Game.id)).filter(models.Game.user_id == user_id, models.Game.result == '0-1').scalar() or 0
    draws = db.query(func.count(models.Game.id)).filter(models.Game.user_id == user_id, models.Game.result == '1/2-1/2').scalar() or 0

    return {
        "username": user.username,
        "elo_rating": user.elo_rating,
        "games_played": games_played,
        "record": {"wins": wins, "losses": losses, "draws": draws}
    }

def get_games_played_this_week(db: Session, user_id: int) -> int:
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(func.count(models.Game.id)).filter(
        models.Game.user_id == user_id,
        models.Game.date_played >= seven_days_ago
    ).scalar() or 0

def get_puzzles_solved_this_week(db: Session, user_id: int) -> int:
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(func.count(models.PuzzleSession.id)).filter(
        models.PuzzleSession.user_id == user_id,
        models.PuzzleSession.is_correct == True,
        models.PuzzleSession.created_at >= seven_days_ago
    ).scalar() or 0

def get_accuracy_history(db: Session, user_id: int, limit: int = 5) -> List[Dict[str, float]]:
    """
    MOCK IMPLEMENTATION: Returns static accuracy data for the last few games.
    A real implementation would calculate this based on move comparison with an engine.
    """
    # In a real scenario, you'd fetch the last 5 games and their analyses
    # and compute the accuracy for each.
    return [
        {"game": 1, "accuracy": 85.2},
        {"game": 2, "accuracy": 91.5},
        {"game": 3, "accuracy": 88.0},
        {"game": 4, "accuracy": 94.1},
        {"game": 5, "accuracy": 92.3},
    ]

# --- Deprecated Functions (to be removed later) ---

def get_recent_games_pgn(db: Session, user_id: int, limit: int = 10) -> list[str]:
    games = (
        db.query(models.Game.pgn)
        .filter(models.Game.user_id == user_id)
        .order_by(models.Game.date_played.desc())
        .limit(limit)
        .all()
    )
    return [game.pgn for game in games]
