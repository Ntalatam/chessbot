from .models import User, Game, Analysis, PuzzleSession, CoachingSession

# This makes the models available when importing from app.models
__all__ = [
    'User',
    'Game',
    'GameAnalysis',
    'Puzzle',
    'PuzzleAttempt',
    'TrainingSession',
]
