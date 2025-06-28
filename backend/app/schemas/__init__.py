from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
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

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool = False
    elo_rating: int = 1200
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Game schemas
class GameBase(BaseModel):
    pgn: str
    fen: Optional[str] = None
    white_player_id: int
    black_player_id: int
    result: Optional[GameResult] = GameResult.UNFINISHED
    time_control: Optional[str] = None
    rated: bool = False

class GameCreate(GameBase):
    pass

class GameInDB(GameBase):
    id: int
    analyzed: bool = False
    created_at: datetime
    analyzed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Analysis schemas
class GameAnalysisBase(BaseModel):
    game_id: int
    accuracy_white: Optional[float] = None
    accuracy_black: Optional[float] = None
    mistakes_white: List[int] = []
    mistakes_black: List[int] = []
    blunders_white: List[int] = []
    blunders_black: List[int] = []
    analysis_pgn: Optional[str] = None

class GameAnalysisCreate(GameAnalysisBase):
    pass

class GameAnalysisInDB(GameAnalysisBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Puzzle schemas
class PuzzleBase(BaseModel):
    fen: str
    moves: List[str]
    rating: int = 1500
    rating_deviation: float = 350.0
    popularity: int = 0
    themes: List[str] = []
    difficulty: PuzzleDifficulty = PuzzleDifficulty.INTERMEDIATE

class PuzzleCreate(PuzzleBase):
    pass

class PuzzleInDB(PuzzleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PuzzleAttemptBase(BaseModel):
    user_id: int
    puzzle_id: int
    success: bool
    time_taken: Optional[float] = None
    moves: Optional[List[str]] = None

class PuzzleAttemptCreate(PuzzleAttemptBase):
    pass

class PuzzleAttemptInDB(PuzzleAttemptBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Training session schemas
class TrainingSessionBase(BaseModel):
    user_id: int
    session_type: str
    focus_area: Optional[str] = None
    duration: Optional[int] = None
    score: Optional[float] = None
    completed: bool = False

class TrainingSessionCreate(TrainingSessionBase):
    pass

class TrainingSessionInDB(TrainingSessionBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Public User schema for responses
class User(UserBase):
    id: int
    elo_rating: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


# User Statistics schema
class UserStats(BaseModel):
    games_played: int
    games_won: int
    games_lost: int
    games_drawn: int
    win_rate: float
    current_streak: int
    highest_elo: int
    favorite_opening: Optional[str] = None
    last_active: Optional[datetime] = None
    account_created: Optional[datetime] = None


# Pagination schema for list responses
class Pagination(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool


# Response schema for user games list
class UserGamesResponse(BaseModel):
    user_id: int
    username: str
    games: List[GameInDB]
    pagination: Pagination

# Request/Response schemas
class AnalysisRequest(BaseModel):
    fen: str
    depth: int = 18

class AnalysisResponse(BaseModel):
    fen: str
    evaluation: Dict[str, Any]
    best_move: Optional[str] = None
    top_moves: List[Dict[str, Any]] = []
    depth: int

class PuzzleRequest(BaseModel):
    user_id: Optional[int] = None
    difficulty: Optional[PuzzleDifficulty] = None
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

class PuzzleAttemptRequest(BaseModel):
    user_id: int
    puzzle_id: int
    success: bool
    time_taken: Optional[float] = None
    moves: Optional[List[str]] = None


class StreamRequest(BaseModel):
    messages: List[Dict[str, str]]


class CoachingRequest(BaseModel):
    user_id: int
    game_pgn: Optional[str] = None
    fen: Optional[str] = None
    question: str
    context: Optional[Dict[str, Any]] = None

class TrainingPlanRequest(BaseModel):
    user_id: int
    time_per_day: int = Field(..., description="Time in minutes per day")
    days_per_week: int = Field(..., ge=1, le=7, description="Days per week")
    focus_areas: List[str] = Field(default_factory=list, description="Areas to focus on")
    current_rating: Optional[int] = None


# Coach schemas
class PlayRequest(BaseModel):
    pgn: str = Field(..., description="The full PGN of the game so far.")


class PlayResponse(BaseModel):
    commentary: str = Field(..., description="The AI coach's commentary on the last move.")
    ai_move: str = Field(..., description="The AI coach's next move in UCI format.")

# WebSocket message schemas
class WSMessageType(str, Enum):
    QUESTION = "question"
    MOVE_SUGGESTION = "move_suggestion"
    POSITION_ANALYSIS = "position_analysis"
    RESPONSE = "response"
    ERROR = "error"

class WSMessage(BaseModel):
    type: WSMessageType
    data: Dict[str, Any] = {}

class WSAnalysisRequest(WSMessage):
    type: WSMessageType = WSMessageType.POSITION_ANALYSIS
    data: Dict[str, str] = Field(..., description="Must contain 'fen' key with position")

class WSMoveSuggestionRequest(WSMessage):
    type: WSMessageType = WSMessageType.MOVE_SUGGESTION
    data: Dict[str, str] = Field(..., description="Must contain 'fen' key with position")

class WSQuestionRequest(WSMessage):
    type: WSMessageType = WSMessageType.QUESTION
    data: Dict[str, str] = Field(..., description="Must contain 'text' key with question")
