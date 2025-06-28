import os
import json
import logging
from typing import Dict, List, Optional, Any, AsyncGenerator
from openai import AsyncOpenAI, OpenAIError
from openai.types.chat import ChatCompletionChunk
from ..core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM service with OpenAI API.

        Args:
            api_key: OpenAI API key. If not provided, will try to get from settings.
        """
        try:
            self.api_key = api_key or settings.OPENAI_API_KEY
            if not self.api_key:
                raise ValueError("OpenAI API key is required")

            # Initialize the client with minimal parameters
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                timeout=30.0,  # Add timeout
            )
            self.model = "gpt-4"  # Default to GPT-4
            logger.info("LLMService initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLMService: {str(e)}")
            raise
        
    async def generate_explanation(self, fen: str, move: str, context: str = "") -> str:
        """Generate a natural language explanation for a chess move.
        
        Args:
            fen: FEN string of the position before the move
            move: Move in UCI format
            context: Optional context about the game or position
            
        Returns:
            Explanation of the move
        """
        prompt = f"""You are a chess grandmaster explaining a move to a student. 
        Explain the move {move} in the following position: {fen}."""
        
        if context:
            prompt += f"\nContext: {context}"
            
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful chess coach that explains moves clearly and concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content.strip() if response.choices[0].message.content else ""
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "I couldn't generate an explanation for that move right now."
    
    async def generate_lesson(self, theme: str, elo: int = 1200) -> Dict[str, str]:
        """Generate a chess lesson on a specific theme.
        
        Args:
            theme: Theme of the lesson (e.g., "Italian Game", "Sicilian Defense")
            elo: Player's approximate rating for difficulty adjustment
            
        Returns:
            Dictionary with lesson content
        """
        prompt = f"""Create a chess lesson about {theme} suitable for a player rated {elo}.
        Include:
        1. A brief introduction to the concept
        2. Main variations and ideas
        3. Common mistakes to avoid
        4. Example positions with explanations
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a chess coach creating educational content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip() if response.choices[0].message.content else ""
            return {
                "title": f"Lesson: {theme}",
                "content": content,
                "difficulty": elo
            }
            
        except Exception as e:
            logger.error(f"Error generating lesson: {e}")
            return {"error": "Failed to generate lesson"}
    
    async def analyze_game(self, pgn: str) -> Dict[str, str]:
        """Analyze a complete game in PGN format.
        
        Args:
            pgn: Game in PGN format
            
        Returns:
            Analysis of the game
        """
        prompt = f"""Analyze the following chess game in PGN format. 
        Highlight key moments, mistakes, and good moves. 
        Provide suggestions for improvement.
        
        {pgn}"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a chess coach analyzing a game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip() if response.choices[0].message.content else ""
            return {
                "analysis": content
            }
            
        except Exception as e:
            logger.error(f"Error analyzing game: {e}")
            return {"error": "Failed to analyze game"}

    async def get_ai_coach_move(self, pgn: str) -> Dict[str, str]:
        """Get the AI coach's move and commentary for a given game state.

        Args:
            pgn: The PGN of the game so far.

        Returns:
            A dictionary containing the AI's commentary and next move.
        """
        prompt = f"""You are a world-class chess grandmaster and a friendly, encouraging coach.
        The user is playing White, and you are playing Black.
        The current game is provided in PGN format below:
        {pgn}

        Your task is to:
        1. Analyze White's last move.
        2. Provide brief, helpful, and encouraging commentary (1-2 sentences max).
        3. Decide on your next move as Black.
        4. Return your response as a JSON object with two keys: "commentary" and "ai_move".

        Example response:
        {{
            "commentary": "Good move! You're controlling the center well. Now, let's see how you handle this.",
            "ai_move": "e7e5"
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful chess coach that responds in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=250,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content.strip() if response.choices[0].message.content else "{}"
            return json.loads(content)

        except Exception as e:
            logger.error(f"Error getting AI coach move: {e}")
            return {"error": "Failed to get AI coach move"}

    async def get_dashboard_insights(self, pgn_list: List[str]) -> Dict[str, any]:
        """Generate dashboard insights based on a list of recent games.

        Args:
            pgn_list: A list of PGN strings from recent games.

        Returns:
            A dictionary containing AI-generated insights.
        """
        if not pgn_list:
            return {
                "strengths": ["Play some games to get your first report!"],
                "improvements": ["We'll identify areas to work on after you've played a few games."],
                "focus": "Your journey starts with the first move. Let's play!"
            }

        games_str = "\n\n".join(pgn_list)
        prompt = f"""You are a master chess coach reviewing a student's recent games.
        Based on the following PGNs, analyze the player's performance and provide a concise "Weekly Report".

        Games:
        {games_str}

        Your analysis should identify:
        1.  **Strengths**: 1-2 key things the player is doing well (e.g., "strong tactical vision in open positions", "excellent endgame technique").
        2.  **Areas for Improvement**: 1-2 specific, actionable weaknesses to work on (e.g., "prone to time trouble in complex middlegames", "could improve pawn structure understanding in the Queen's Gambit").
        3.  **Weekly Focus**: A single, encouraging sentence suggesting what to focus on for the next week.

        Return your response as a JSON object with three keys: "strengths" (a list of strings), "improvements" (a list of strings), and "focus" (a single string).

        Example response:
        {{
            "strengths": ["You have a strong command of endgame scenarios, frequently converting small advantages into wins."],
            "improvements": ["Your openings could be more varied. You tend to play the same e4 openings, making you predictable.", "Watch out for simple tactical blunders in the middlegame under time pressure."],
            "focus": "This week, let's focus on expanding your opening repertoire. Try the Sicilian Defense in a few games!"
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful and insightful chess coach that responds in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content.strip() if response.choices[0].message.content else "{}"
            return json.loads(content)

        except Exception as e:
            logger.error(f"Error generating dashboard insights: {e}")
            return {"error": "Failed to generate AI insights"}

    def get_system_prompt(self) -> Dict[str, str]:
        """Returns the system prompt for the AI coach."""
        return {
            "role": "system",
            "content": """You are a world-class, personalized chess coach—on the level of Magnus Carlsen’s personal trainer. Your role is to guide me interactively and dynamically to become a top-tier chess player. Adapt your coaching to my current level, weaknesses, and goals, and evolve with me over time. Assume I am around 400 rapid on Chess.com, with the goal of reaching 800 within the year—and eventually, becoming a grandmaster with your help.

Your responsibilities include:
- Asking diagnostic questions to assess my playing style and weaknesses
- Creating and adjusting a customized weekly training plan
- Providing tactical exercises, endgame drills, and strategic lessons
- Helping build and refine my opening repertoire based on my style
- Analyzing my games (via PGN or summaries)
- Teaching me to think like a Grandmaster—using clear, practical explanations
- Preparing me for tournament or online play (including mindset and time management)
- Offering feedback, performance reviews, and suggested next steps

You should be supportive but rigorous—like a real mentor. Use examples, board visualizations (if possible), and ask reflective questions to improve retention. If I plateau, adjust your coaching strategy. Above all, drive the training forward proactively.

Start by asking me a few questions to assess my strengths, weaknesses, and learning preferences, then propose how we’ll structure the first week of training.
Make sure this is passed as the system role when initializing the message array."""
        }

    async def stream_chat_response(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        """Streams a chat response from the OpenAI API with detailed logging."""
        logger.info("--- [LLM Service] Starting stream_chat_response ---")
        
        # Validate API key
        if not hasattr(self, 'api_key') or not self.api_key:
            error_msg = "OpenAI API key is not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        # Validate messages
        if not messages or not isinstance(messages, list):
            error_msg = "Messages must be a non-empty list of message objects"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        for msg in messages:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                error_msg = f"Invalid message format: {msg}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        # Prepare messages with system prompt
        try:
            system_prompt = self.get_system_prompt()
            all_messages = [system_prompt] + messages
            
            # Log the request (without sensitive data)
            log_messages = [
                {k: v for k, v in msg.items() if k in ['role', 'content']} 
                for msg in all_messages
            ]
            logger.info(f"[LLM Service] Sending request to OpenAI with {len(log_messages)} messages")
            logger.debug(f"[LLM Service] Messages: {log_messages}")
            
            # Make the API call
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=all_messages,
                stream=True,
                temperature=0.7,
                max_tokens=1000
            )
            
            logger.info("[LLM Service] Successfully connected to OpenAI API")
            
            # Stream the response
            async for chunk in stream:
                if not isinstance(chunk, ChatCompletionChunk):
                    continue
                    
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
            
            logger.info("[LLM Service] Stream completed successfully")
            
        except OpenAIError as e:
            error_msg = f"OpenAI API error: {str(e)}"
            logger.error(f"[LLM Service] {error_msg}", exc_info=True)
            yield f"[ERROR] {error_msg}"
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"[LLM Service] {error_msg}", exc_info=True)
            yield f"[ERROR] {error_msg}"
