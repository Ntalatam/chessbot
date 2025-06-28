from datetime import datetime, timedelta
import logging
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import models, schemas
from ..core.config import settings
from ..core.security import (
    create_access_token,
    get_password_hash,
    get_current_user,
    oauth2_scheme,
    verify_password,
)
from ..db import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/register",
    response_model=schemas.UserInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_description="The created user"
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """
    Register a new user.

    Args:
        user: User creation data
        db: Database session

    Returns:
        The created user

    Raises:
        HTTPException: If user with email already exists or username is taken
    """
    # Check if user with email already exists
    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username is taken
    db_user_by_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        elo_rating=1200,
        is_active=True,
        is_superuser=False
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"Integrity error during user registration: {ie}")
        # If unique constraint fails despite our earlier checks
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given email or username already exists"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return db_user

@router.post(
    "/token",
    response_model=schemas.Token,
    summary="OAuth2 token login",
    description="OAuth2 compatible token login, get an access token for future requests",
    response_description="The access token and token type"
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> schemas.Token:
    """
    OAuth2 compatible token login, get an access token for future requests.

    Args:
        form_data: The OAuth2 password request form containing username and password
        db: Database session

    Returns:
        Dictionary containing the access token and token type

    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return schemas.Token(access_token=access_token, token_type="bearer")

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """
    Authenticate a user with username and password.

    Args:
        db: Database session
        username: User's username
        password: Plain text password

    Returns:
        User object if authentication is successful, None otherwise
    """
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for username: {username}")
            return None
        return user
    except Exception as e:
        logger.error(f"Error authenticating user {username}: {str(e)}")
        return None

@router.get(
    "/users/me",
    response_model=schemas.UserInDB,
    summary="Get current user",
    description="Get information about the currently authenticated user",
    response_description="The current user's information"
)
async def read_users_me(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    Get current user information.

    Args:
        current_user: The currently authenticated user (injected by dependency)

    Returns:
        The current user's information
    """
    return current_user

@router.put(
    "/users/me",
    response_model=schemas.UserInDB,
    summary="Update current user",
    description="Update the currently authenticated user's information",
    response_description="The updated user information"
)
async def update_user_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Update current user information.

    Args:
        user_update: The user data to update
        current_user: The currently authenticated user (injected by dependency)
        db: Database session

    Returns:
        The updated user information

    Raises:
        HTTPException: If there's an error updating the user
    """
    try:
        update_data = user_update.dict(exclude_unset=True)
        
        # If password is being updated, hash it
        if 'password' in update_data:
            if not update_data['password']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password cannot be empty"
                )
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
        
        # Update user data
        for field, value in update_data.items():
            if hasattr(current_user, field):
                setattr(current_user, field, value)
        
        current_user.updated_at = datetime.utcnow()
        
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"User {current_user.email} updated their profile")
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user {current_user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user information"
        )

@router.get(
    "/{user_id}",
    response_model=schemas.UserInDB,
    summary="Get user by ID",
    description="Get user information by ID (admin only)",
    response_description="The requested user's information"
)
async def get_user(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Get user by ID (admin only).

    Args:
        user_id: The ID of the user to retrieve
        current_user: The currently authenticated user (injected by dependency)
        db: Database session

    Returns:
        The requested user's information

    Raises:
        HTTPException: If user doesn't have permission or user not found
    """
    # Only allow admins to access user details
    if not current_user.is_superuser:
        logger.warning(f"User {current_user.id} attempted to access user {user_id} without permission")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"Admin {current_user.id} accessed user {user_id} details")
    return user

@router.get(
    "/{user_id}/stats",
    response_model=schemas.UserStats,
    summary="Get user statistics",
    description="Get statistics for a specific user (user can only see their own stats unless admin)",
    response_description="The requested user's statistics"
)
async def get_user_stats(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user statistics.

    Args:
        user_id: The ID of the user to get statistics for
        current_user: The currently authenticated user (injected by dependency)
        db: Database session

    Returns:
        Dictionary containing the user's statistics

    Raises:
        HTTPException: If user doesn't have permission or user not found
    """
    # Only allow users to view their own stats or admins
    if user_id != current_user.id and not current_user.is_superuser:
        logger.warning(f"User {current_user.id} attempted to access stats for user {user_id} without permission")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view these stats"
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"User with ID {user_id} not found when fetching stats")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # Calculate statistics (placeholder values for now)
        # In a real application, you would query the database for these values
        stats = {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "games_drawn": 0,
            "win_rate": 0.0,
            "current_streak": 0,
            "highest_elo": user.elo_rating,
            "favorite_opening": None,
            # "last_active": user.last_login_at.isoformat() if user.last_login_at else None, # Field not in model
            "account_created": user.created_at.isoformat() if user.created_at else None
        }
        
        logger.info(f"Retrieved stats for user {user_id}")
        return stats
        
    except Exception as e:
        logger.error(f"Error fetching stats for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )
    return stats

@router.get(
    "/{user_id}/games",
    response_model=schemas.UserGamesResponse,
    summary="Get user's games",
    description="Get paginated list of games for a specific user",
    response_description="Paginated list of the user's games"
)
async def get_user_games(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get games for a specific user with pagination.

    Args:
        user_id: The ID of the user to get games for
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        current_user: The currently authenticated user (injected by dependency)
        db: Database session

    Returns:
        Dictionary containing paginated list of games and metadata

    Raises:
        HTTPException: If user doesn't have permission or user not found
    """
    # Verify the user has permission to view these games
    if user_id != current_user.id and not current_user.is_superuser:
        logger.warning(f"User {current_user.id} attempted to access games for user {user_id} without permission")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these games"
        )
    
    # Validate pagination parameters
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip parameter cannot be negative"
        )
    
    if limit <= 0 or limit > 100:  # Enforce a reasonable limit
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"User with ID {user_id} not found when fetching games")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # In a real app, you would query the database for the user's games with pagination
        # This is a placeholder implementation
        total_games = 0  # Would be set by a database count query
        games = []  # Would be populated by a database query with limit/offset
        
        logger.info(f"Retrieved {len(games)} games for user {user_id}")
        
        return {
            "user_id": user.id,
            "username": user.username,
            "games": games,
            "pagination": {
                "total": total_games,
                "skip": skip,
                "limit": limit,
                "has_more": (skip + len(games)) < total_games
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching games for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user games"
        )
