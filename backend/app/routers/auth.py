from fastapi import APIRouter, Depends, HTTPException, status
import logging

logger = logging.getLogger(__name__)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import schemas, crud, models
from ..core import security
from ..db import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: '{user.email}', username: '{user.username}'")

    # Normalize inputs
    normalized_email = user.email.strip().lower()
    normalized_username = user.username.strip().lower()
    logger.info(f"Normalized inputs - email: '{normalized_email}', username: '{normalized_username}'")

    # Check for duplicate email
    existing_email = crud.user.get_user_by_email(db, email=normalized_email)
    logger.info(f"Checking for existing email ('{normalized_email}'): Found -> {existing_email is not None}")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check for duplicate username
    existing_username = crud.user.get_user_by_username(db, username=normalized_username)
    logger.info(f"Checking for existing username ('{normalized_username}'): Found -> {existing_username is not None}")
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create a new UserCreate instance with normalized data to pass to the CRUD function
    user_in = schemas.UserCreate(email=normalized_email, username=normalized_username, password=user.password)

    logger.info(f"No duplicates found. Proceeding to create user '{normalized_username}'.")
    try:
        created_user = crud.user.create_user(db=db, user=user_in)
        return created_user
    except IntegrityError:
        db.rollback()  # Rollback the session to a clean state
        logger.error(f"Database integrity error for email '{normalized_email}' or username '{normalized_username}'.")
        raise HTTPException(
            status_code=409, # 409 Conflict is more appropriate here
            detail="This email or username is already registered at the database level.",
        )

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.get_user_by_email(db, email=form_data.username) # OAuth2PasswordRequestForm uses 'username' for the email field
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
