import math
from typing import Tuple, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class EloService:
    def __init__(self, k_factor: int = 32, default_rating: int = 1200):
        """Initialize the Elo rating service.
        
        Args:
            k_factor: Maximum adjustment per game (higher = more volatile ratings)
            default_rating: Starting rating for new players
        """
        self.k_factor = k_factor
        self.default_rating = default_rating
    
    def expected_score(self, rating_a: int, rating_b: int) -> float:
        """Calculate the expected score between two ratings.
        
        Args:
            rating_a: First player's rating
            rating_b: Second player's rating
            
        Returns:
            Expected score for player A (0-1)
        """
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    def calculate_new_ratings(
        self, 
        player_rating: int, 
        opponent_rating: int, 
        score: float
    ) -> Tuple[int, int]:
        """Calculate new ratings after a game.
        
        Args:
            player_rating: Player's current rating
            opponent_rating: Opponent's current rating
            score: 1 for win, 0.5 for draw, 0 for loss
            
        Returns:
            Tuple of (new_player_rating, new_opponent_rating)
        """
        expected = self.expected_score(player_rating, opponent_rating)
        
        # Calculate rating changes
        player_change = self.k_factor * (score - expected)
        opponent_change = self.k_factor * ((1 - score) - (1 - expected))
        
        # Update ratings
        new_player_rating = round(player_rating + player_change)
        new_opponent_rating = round(opponent_rating + opponent_change)
        
        return new_player_rating, new_opponent_rating
    
    def calculate_performance_rating(
        self, 
        results: List[Dict[str, Any]], 
        initial_guess: int = 1500
    ) -> int:
        """Calculate performance rating based on game results.
        
        Args:
            results: List of dicts with 'opponent_rating' and 'score' (0-1)
            initial_guess: Starting point for iteration
            
        Returns:
            Performance rating (integer)
        """
        if not results:
            return self.default_rating
            
        # Simple average for small number of games
        if len(results) <= 4:
            total = 0
            total_score = 0.0
            for result in results:
                total += result['opponent_rating']
                total_score += result['score']
            return round(total / len(results) + 400 * (total_score / len(results) - 0.5))
            
        # Iterative calculation for more games
        rating = initial_guess
        for _ in range(20):  # Maximum iterations
            sum_expected = 0.0
            sum_actual = 0.0
            
            for result in results:
                expected = self.expected_score(rating, result['opponent_rating'])
                sum_expected += expected
                sum_actual += result['score']
                
            new_rating = rating + self.k_factor * (sum_actual - sum_expected)
            
            # Check for convergence
            if abs(new_rating - rating) < 1:
                break
                
            rating = new_rating
            
        return round(rating)
    
    def calculate_rating_deviation(
        self, 
        results: List[Dict[str, Any]], 
        current_rating: int
    ) -> float:
        """Calculate rating deviation (uncertainty) based on recent results.
        
        Args:
            results: List of recent game results
            current_rating: Player's current rating
            
        Returns:
            Standard deviation of rating estimate
        """
        if len(results) < 5:
            # Higher uncertainty for few games
            return 200.0
            
        squared_errors = []
        for result in results[-10:]:  # Use last 10 games
            expected = self.expected_score(
                current_rating, 
                result['opponent_rating']
            )
            error = result['score'] - expected
            squared_errors.append(error ** 2)
            
        if not squared_errors:
            return 200.0
            
        mean_squared_error = sum(squared_errors) / len(squared_errors)
        return math.sqrt(mean_squared_error) * 400  # Scale to rating points
