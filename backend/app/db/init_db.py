import logging
import sys
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import session
from ..models import models
from ..models.models import User, Puzzle, Analysis
from ..schemas import schemas
from ..core.security import get_password_hash
from ..core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """
    Initialize the database with initial data.
    """
    try:
        # Create tables
        logger.info("Creating database tables...")
        models.Base.metadata.create_all(bind=session.engine)
        
        # Create admin user if it doesn't exist
        admin_email = settings.FIRST_SUPERUSER_EMAIL
        admin_password = settings.FIRST_SUPERUSER_PASSWORD
        
        if not admin_email or not admin_password:
            logger.warning(
                "FIRST_SUPERUSER_EMAIL and FIRST_SUPERUSER_PASSWORD not set. "
                "Skipping admin user creation."
            )
        else:
            user = db.query(models.User).filter(models.User.email == admin_email).first()
            if not user:
                logger.info("Creating initial admin user...")
                admin_user = models.User(
                    email=admin_email,
                    username="admin",
                    hashed_password=get_password_hash(admin_password),
                    is_superuser=True,
                    is_active=True,
                    elo_rating=2000
                )
                db.add(admin_user)
                db.commit()
                logger.info("Admin user created successfully")
            else:
                logger.info("Admin user already exists")
        
        # Add initial puzzles if none exist
        if db.query(models.Puzzle).count() == 0:
            logger.info("Adding initial puzzles...")
            initial_puzzles = [
                {
                    "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 0 1",
                    "moves": ["f6e4", "d1d8"],
                    "rating": 1500,
                    "themes": ["fork", "tactics"],
                    "difficulty": "intermediate"
                },
                {
                    "fen": "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPPB1PPP/R2QK2R w KQ - 0 1",
                    "moves": ["c3d5", "f6d5", "c4d5"],
                    "rating": 1600,
                    "themes": ["tactics", "fork"],
                    "difficulty": "intermediate"
                },
                {
                    "fen": "r1bq1rk1/ppp2ppp/2n2n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 1",
                    "moves": ["f3e5", "c6e5", "d1d8", "f8d8", "c4f7", "e8f7", "c3e4"],
                    "rating": 1700,
                    "themes": ["tactics", "fork", "skewer"],
                    "difficulty": "advanced"
                },
                {
                    "fen": "r1bq1rk1/ppp2ppp/2n2n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 1",
                    "moves": ["f3e5", "c6e5", "d1d8", "f8d8", "c4f7", "e8f7", "c3e4"],
                    "rating": 1700,
                    "themes": ["tactics", "fork", "skewer"],
                    "difficulty": "advanced"
                },
                {
                    "fen": "r1bq1rk1/ppp2ppp/2n2n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 1",
                    "moves": ["f3e5", "c6e5", "d1d8", "f8d8", "c4f7", "e8f7", "c3e4"],
                    "rating": 1700,
                    "themes": ["tactics", "fork", "skewer"],
                    "difficulty": "advanced"
                },
            ]
            
            for puzzle_data in initial_puzzles:
                puzzle = models.Puzzle(**puzzle_data)
                db.add(puzzle)
            
            db.commit()
            logger.info(f"Added {len(initial_puzzles)} initial puzzles")
        else:
            logger.info("Puzzles already exist in the database")
            
        # Create initial analysis cache entries if needed
        if db.query(models.Analysis).count() == 0:
            logger.info("Adding initial analysis cache entries...")
            initial_positions = [
                {
                    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                    "depth": 18,
                    "evaluation": {"value": 0.2, "type": "cp"},
                    "best_move": "e2e4"
                },
                {
                    "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
                    "depth": 18,
                    "evaluation": {"value": 0.3, "type": "cp"},
                    "best_move": "g1f3"
                }
            ]
            
            for analysis_data in initial_positions:
                analysis = models.Analysis(**analysis_data)
                db.add(analysis)
            
            db.commit()
            logger.info(f"Added {len(initial_positions)} initial analysis cache entries")
        else:
            logger.info("Analysis cache entries already exist")
            
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error initializing database: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error initializing database: {str(e)}")
        raise

def reset_db() -> None:
    """
    Drop all tables and recreate them.
    WARNING: This will delete all data in the database!
    """
    try:
        logger.warning("Dropping all tables...")
        models.Base.metadata.drop_all(bind=session.engine)
        logger.info("Recreating tables...")
        models.Base.metadata.create_all(bind=session.engine)
        logger.info("Database reset complete")
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        raise

if __name__ == "__main__":
    # Initialize the database
    db = session.SessionLocal()
    try:
        import argparse
        
        parser = argparse.ArgumentParser(description="Database initialization utility")
        parser.add_argument(
            "--reset", 
            action="store_true", 
            help="Reset the database (drop all tables and recreate)"
        )
        args = parser.parse_args()
        
        if args.reset:
            reset_db()
        
        # Always run init_db to ensure required data exists
        init_db(db)
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        db.close()
