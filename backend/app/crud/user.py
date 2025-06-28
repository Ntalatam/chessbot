from sqlalchemy.orm import Session

from .. import models, schemas
from ..core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email.strip().lower()).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username.strip().lower()).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
