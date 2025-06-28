from pydantic import BaseModel
from typing import List, Dict

# --- Main Dashboard Schemas ---

class UserProfile(BaseModel):
    username: str
    elo: int
    games_played: int
    record: Dict[str, int] # e.g., {"wins": 10, "losses": 5, "draws": 3}

class ProgressSummary(BaseModel):
    games_played_this_week: int
    puzzles_solved_this_week: int
    # Using a simple dict for accuracy chart for now
    accuracy_history: List[Dict[str, float]] # e.g., [{"game": 1, "accuracy": 85.2}, ...]

class AICoachingTip(BaseModel):
    title: str
    message: str

class NewDashboardData(BaseModel):
    user_profile: UserProfile
    progress_summary: ProgressSummary
    coaching_feed: List[AICoachingTip]


# --- Schemas for API sub-responses (can be deprecated later) ---

class DashboardStats(BaseModel):
    elo: int
    games_played: int
    record: Dict[str, int]

class AIInsights(BaseModel):
    strengths: List[str]
    improvements: List[str]
    focus: str

class EloDataPoint(BaseModel):
    date: str
    elo: int

class DashboardCoreData(BaseModel):
    stats: DashboardStats
    elo_history: List[EloDataPoint]
