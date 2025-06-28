from typing import Dict, Any, Optional
import chess
from stockfish import Stockfish
import logging

logger = logging.getLogger(__name__)

class EngineService:
    def __init__(self, stockfish_path: str = "stockfish"):
        """Initialize the chess engine service.
        
        Args:
            stockfish_path: Path to the Stockfish executable or 'stockfish' if in PATH
        """
        try:
            self.stockfish = Stockfish(stockfish_path)
            self.stockfish.set_depth(18)
            self.stockfish.set_skill_level(20)  # Max skill level
        except Exception as e:
            logger.error(f"Failed to initialize Stockfish: {e}")
            raise RuntimeError("Failed to initialize chess engine")

    def analyze_position(self, fen: str, depth: int = 18) -> Dict[str, Any]:
        """Analyze a chess position.
        
        Args:
            fen: FEN string of the position
            depth: Search depth
            
        Returns:
            Dictionary with evaluation details
        """
        try:
            if not self.stockfish.is_fen_valid(fen):
                raise ValueError("Invalid FEN string")
                
            self.stockfish.set_fen_position(fen)
            evaluation = self.stockfish.get_evaluation()
            
            return {
                'fen': fen,
                'evaluation': evaluation,
                'best_move': self.stockfish.get_best_move(),
                'top_moves': self.stockfish.get_top_moves(3),
                'depth': depth
            }
            
        except Exception as e:
            logger.error(f"Error analyzing position: {e}")
            raise

    def get_best_move(self, fen: str, depth: int = 18) -> Optional[str]:
        """Get the best move for a given position.
        
        Args:
            fen: FEN string of the position
            depth: Search depth
            
        Returns:
            Best move in UCI format or None if no legal moves
        """
        try:
            board = chess.Board(fen)
            if board.is_game_over():
                return None
                
            self.stockfish.set_fen_position(fen)
            self.stockfish.set_depth(depth)
            return self.stockfish.get_best_move()
            
        except Exception as e:
            logger.error(f"Error getting best move: {e}")
            raise

    def is_move_correct(self, fen: str, move_uci: str) -> bool:
        """Check if a move is the best or one of the top moves.
        
        Args:
            fen: FEN string of the position
            move_uci: Move in UCI format to check
            
        Returns:
            bool: True if the move is among the top moves
        """
        try:
            self.stockfish.set_fen_position(fen)
            best_move = self.stockfish.get_best_move()
            return move_uci.lower() == best_move.lower()
        except Exception as e:
            logger.error(f"Error checking move: {e}")
            return False
