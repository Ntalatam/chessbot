from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import json
import asyncio
import logging
import openai

from .. import schemas
from ..services.llm_service import LLMService
from ..core.config import settings
from ..services.engine_service import EngineService
from ..models.models import Game, User, CoachingSession
from ..db import get_db, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/stream_ask", description="Ask the AI coach a question and get a streaming response.")
async def stream_ask_coach(request: schemas.StreamRequest):
    """
    Handles a streaming chat request with the AI coach.
    """
    try:
        logger.info(f"[AI Coach API] Received payload: {request.dict()}")
        llm_service = LLMService(api_key=settings.OPENAI_API_KEY)
        logger.info("[AI Coach API] Initiating stream with OpenAI.")
        return StreamingResponse(llm_service.stream_chat_response(request.messages), media_type="text/event-stream")
    except openai.APIError as e:
        logger.error(f"[AI Coach API] OpenAI API error: {e}", exc_info=True)
        raise HTTPException(status_code=502, detail=f"Failed to get response from AI provider: {e}")
    except Exception as e:
        logger.error(f"[AI Coach API] An unexpected error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing your request.")

@router.post("/ask")
async def ask_coach(request: schemas.CoachingRequest):
    """
    Ask the AI coach a question about chess. No user account required.
    """
    try:
        llm_service = LLMService()
        engine_service = EngineService()
        
        context = {
            "user_rating": request.user_rating,
            "question": request.question
        }
        
        if request.context:
            context.update(request.context)
        
        if request.fen:
            try:
                analysis = engine_service.analyze_position(request.fen)
                context["position_analysis"] = {
                    "evaluation": analysis.get("evaluation"),
                    "best_move": analysis.get("best_move"),
                    "top_moves": analysis.get("top_moves", [])
                }
            except Exception as e:
                logger.error(f"Error analyzing position: {e}")
        
        response = await llm_service.generate_explanation(
            fen=request.fen or "",
            move="",
            context=json.dumps(context)
        )
        
        return {"response": response}
        
    except Exception as e:
        logger.error(f"Error in ask_coach: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-game")
async def analyze_game(game_pgn: str):
    """
    Analyze a complete game and provide feedback. No user account required.
    """
    try:
        llm_service = LLMService()
        analysis = await llm_service.analyze_game(game_pgn)
        
        return {
            "success": True,
            "analysis": analysis.get("analysis", "Analysis not available"),
        }
    except Exception as e:
        logger.error(f"Error analyzing game: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-training-plan")
async def create_training_plan(request: schemas.TrainingPlanRequest):
    """
    Create a personalized training plan. No user account required.
    """
    try:
        prompt = f"""Create a personalized chess training plan for a player currently 
        rated {request.current_rating} who can spend {request.time_per_day} minutes per day. """
        
        if request.focus_areas:
            prompt += f"Focus areas: {', '.join(request.focus_areas)}. "
            
        prompt += """
        The plan should include:
        1. Daily training schedule
        2. Specific exercises or concepts to focus on
        3. Recommended time allocation for each activity
        4. Weekly goals
        """
        
        # This is a placeholder. In a real app, you would use the LLM service.
        plan = {
            "weekly_schedule": {
                "monday": "Tactics (30m), Endgame practice (20m)",
                "tuesday": "Game analysis (30m), Opening study (20m)",
                "wednesday": "Tactics (30m), Strategy (20m)",
                "thursday": "Rest day",
                "friday": "Play games (50m)",
                "saturday": "Review games (30m), Tactics (20m)",
                "sunday": "Full game with analysis (60m)"
            },
            "focus_areas": request.focus_areas or ["Tactics", "Positional play", "Endgames"],
            "weekly_goals": [
                "Solve 30 tactical puzzles",
                "Analyze 2 of your own games",
                "Study 1 new opening variation",
                "Practice 3 endgame positions"
            ]
        }
        
        # Database saving logic is removed as there is no user.
        
        return {
            "success": True,
            "plan": plan,
        }
        
    except Exception as e:
        logger.error(f"Error creating training plan: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play", response_model=schemas.PlayResponse)
async def get_ai_coach_move(play_request: schemas.PlayRequest) -> schemas.PlayResponse:
    """
    Play a move against the AI coach and get commentary and the AI's next move.
    """
    logger.info(f"Received request for AI coach move with PGN: {play_request.pgn}")
    try:
        llm_service = LLMService()
        ai_response = await llm_service.get_ai_coach_move(play_request.pgn)

        if not ai_response or "ai_move" not in ai_response:
            logger.error("AI response was empty or did not contain a move.")
            raise HTTPException(status_code=500, detail="AI failed to generate a valid move.")

        logger.info(f"AI generated move: {ai_response['ai_move']} with commentary: {ai_response['commentary']}")
        return schemas.PlayResponse(**ai_response)

    except Exception as e:
        logger.error(f"Error getting AI coach move: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get AI move from coach.")

