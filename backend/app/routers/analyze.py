from fastapi import APIRouter, HTTPException, Depends, status, Query, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import chess
import chess.pgn
import logging
from datetime import datetime

from ..services.engine_service import EngineService
# User-related imports are no longer needed
# from ..core.security import get_current_user
# from ..db.session import get_db
# from sqlalchemy.orm import Session
# from ..models.models import Analysis, User
from ..schemas import AnalysisRequest, AnalysisResponse, WSAnalysisRequest

router = APIRouter(prefix="/analyze", tags=["analysis"])
logger = logging.getLogger(__name__)

# Initialize engine service
engine_service = EngineService()

class PositionAnalysisRequest(AnalysisRequest):
    """Request model for position analysis"""
    multipv: int = Field(default=3, ge=1, le=5, description="Number of top moves to return")
    lines: Optional[List[str]] = Field(
        default=None, 
        description="Specific lines/variations to analyze"
    )

class GameAnalysisRequest(BaseModel):
    """Request model for full game analysis"""
    pgn: str = Field(..., description="PGN of the game to analyze")
    depth: int = Field(default=18, ge=5, le=30, description="Search depth")
    multi_pv: int = Field(default=3, ge=1, le=5, description="Number of top moves to consider")
    analyze_interval: int = Field(
        default=3, 
        ge=1, 
        le=10, 
        description="Analyze every N moves (1 = every move)"
    )

@router.post("/position", response_model=AnalysisResponse)
async def analyze_position(request: PositionAnalysisRequest) -> AnalysisResponse:
    """
    Analyze a chess position with Stockfish
    
    Returns:
        AnalysisResponse: Detailed analysis of the position
    """
    try:
        # Validate FEN
        try:
            board = chess.Board(request.fen)
            if not board.is_valid():
                raise ValueError("Invalid FEN string")
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid FEN: {str(e)}"
            )
        
        logger.info(f"Analyzing position for FEN: {request.fen}")
        
        # Get analysis from engine
        analysis = engine_service.analyze_position(
            fen=request.fen,
            depth=request.depth,
            multipv=request.multipv,
            lines=request.lines
        )
        
        # Database saving logic is removed as there is no user.
        
        return AnalysisResponse(
            fen=request.fen,
            evaluation=analysis,
            best_move=analysis.get("best_move"),
            top_moves=analysis.get("top_moves", [])
        )
        
    except Exception as e:
        logger.error(f"Error analyzing position: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing position: {str(e)}"
        )

@router.post("/game")
async def analyze_game(request: GameAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze a complete chess game
    
    Returns:
        Dict containing analysis of key positions in the game
    """
    try:
        # Parse PGN
        game = chess.pgn.read_game(request.pgn.split('\n'))
        if not game:
            raise ValueError("Invalid PGN")
            
        board = game.board()
        analysis_results = []
        move_count = 0
        
        # Iterate through all moves in the game
        for move in game.mainline_moves():
            board.push(move)
            move_count += 1
            
            # Only analyze at specified intervals
            if move_count % request.analyze_interval != 0:
                continue
                
            # Analyze position
            fen = board.fen()
            analysis = engine_service.analyze_position(
                fen=fen,
                depth=request.depth,
                multipv=request.multi_pv
            )
            
            analysis_results.append({
                "move_number": (move_count + 1) // 2,
                "move_color": "white" if move_count % 2 == 1 else "black",
                "fen": fen,
                "move": move.uci(),
                "analysis": analysis
            })
        
        return {
            "success": True,
            "analysis": analysis_results,
            "total_positions_analyzed": len(analysis_results)
        }
        
    except Exception as e:
        logger.error(f"Error analyzing game: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing game: {str(e)}"
        )

@router.websocket("/ws/analyze")
async def websocket_analysis(
    websocket: WebSocket,
    depth: int = Query(18, ge=5, le=30)
):
    """
    WebSocket endpoint for real-time position analysis
    """
    await websocket.accept()
    
    try:
        logger.info(f"Anonymous WebSocket connection established for analysis.")
        
        while True:
            try:
                # Wait for messages from client
                data = await websocket.receive_json()
                request = WSAnalysisRequest(**data)
                
                # Handle different message types
                if request.type == "position_analysis":
                    fen = request.data.get("fen")
                    if not fen:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Missing FEN in position analysis request"
                        })
                        continue
                        
                    # Analyze position
                    analysis = engine_service.analyze_position(
                        fen=fen,
                        depth=depth
                    )
                    
                    # Send analysis back to client
                    await websocket.send_json({
                        "type": "analysis_result",
                        "fen": fen,
                        "analysis": analysis
                    })
                    
            except WebSocketDisconnect:
                logger.info(f"Anonymous analysis WebSocket disconnected")
                break
                
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}", exc_info=True)
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error: {str(e)}"
                })
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}", exc_info=True)
    finally:
        await websocket.close()

# Backward compatibility endpoints
@router.get("/best_move/{fen}")
async def get_best_move(
    fen: str, 
    depth: int = Query(18, ge=5, le=30)
) -> Dict[str, Any]:
    """
    Get the best move for a given position (legacy endpoint)
    """
    try:
        best_move = engine_service.get_best_move(fen, depth)
        evaluation = engine_service.analyze_position(fen, depth)
        
        return {
            "success": True,
            "best_move": best_move,
            "evaluation": evaluation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
