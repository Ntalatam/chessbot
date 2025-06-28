from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, models
from ..core.security import get_current_active_user
from ..db.session import get_db
from ..schemas.dashboard import (
    AICoachingTip,
    NewDashboardData,
    ProgressSummary,
    UserProfile,
)

router = APIRouter()


@router.get("/", response_model=NewDashboardData)
async def get_new_dashboard_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> NewDashboardData:
    """
    Retrieve all data required for the new, feature-rich user dashboard.
    """
    # 1. Fetch User Profile
    user_profile_data = crud.dashboard.get_user_profile_data(db, user_id=current_user.id)
    user_profile = UserProfile(**user_profile_data)

    # 2. Fetch Progress Summary
    games_this_week = crud.dashboard.get_games_played_this_week(
        db, user_id=current_user.id
    )
    puzzles_this_week = crud.dashboard.get_puzzles_solved_this_week(
        db, user_id=current_user.id
    )
    accuracy_history = crud.dashboard.get_accuracy_history(db, user_id=current_user.id)

    progress_summary = ProgressSummary(
        games_played_this_week=games_this_week,
        puzzles_solved_this_week=puzzles_this_week,
        accuracy_history=accuracy_history,
    )

    # 3. Fetch AI Coaching Feed (Mocked for now)
    coaching_tips_data = [
        {
            "title": "Opening Principle",
            "message": "Control the center early in the game to gain a strategic advantage.",
        },
        {
            "title": "Tactical Awareness",
            "message": "Always look for checks, captures, and threats before making your move.",
        },
        {
            "title": "Endgame Tip",
            "message": "In king and pawn endgames, the activity of your king is often the most important factor.",
        },
    ]
    coaching_feed = [AICoachingTip(**tip) for tip in coaching_tips_data]

    # 4. Assemble and return the final dashboard data
    return NewDashboardData(
        user_profile=user_profile,
        progress_summary=progress_summary,
        coaching_feed=coaching_feed,
    )
