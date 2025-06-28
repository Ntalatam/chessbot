import os
import json
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse, StreamingResponse
import httpx
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..core.config import settings
from ..models.models import Game, User, CoachingSession
from ..db import get_db, SessionLocal
from .. import schemas
from ..services.engine_service import EngineService

router = APIRouter()

# Simple test endpoint to verify the router is working
@router.get("/test")
async def test_endpoint():
    return {"status": "ok", "message": "Coach router is working"}

async def test_openai():
    """Test endpoint to verify OpenAI connectivity."""
    try:
        # Use direct HTTP request to avoid client issues
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say this is a test"}],
            "max_tokens": 10
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "response": result["choices"][0]["message"]["content"]
                }
            else:
                return {
                    "status": "error",
                    "error": {
                        "status_code": response.status_code,
                        "details": response.text
                    }
                }
                
    except Exception as e:
        logger.error(f"OpenAI test failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": {
                "message": str(e),
                "type": type(e).__name__
            }
        }

@router.get("/test-openai")
async def test_openai_endpoint():
    """Test endpoint to verify OpenAI connectivity."""
    return await test_openai()

@router.post("/direct-chat")
async def direct_chat(request: Request):
    """Direct chat endpoint using HTTPX instead of OpenAI client."""
    try:
        # Get the request data
        data = await request.json()
        messages = data.get("messages", [])
        
        if not messages:
            return JSONResponse(
                status_code=400,
                content={"error": "No messages provided"}
            )
        
        # Prepare the OpenAI API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        # Make the request to OpenAI
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "response": result["choices"][0]["message"]["content"]
                }
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "error": "OpenAI API request failed",
                        "details": response.text
                    }
                )
                
    except Exception as e:
        logger.error(f"Direct chat error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "An error occurred",
                "details": str(e)
            }
        )

@router.post("/ask")
async def ask_coach(request: schemas.CoachingRequest):
    """
    Handles a non-streaming chat request with the AI coach.
    """
    try:
        logger.info(f"[AI Coach API] Received ask request: {request.dict()}")
        
        # Prepare the OpenAI API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful chess coach."},
                {"role": "user", "content": request.prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        # Make the request to OpenAI
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OpenAI API error: {response.text}"
                )
                
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

