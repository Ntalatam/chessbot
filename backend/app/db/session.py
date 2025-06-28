import logging
from typing import Generator, Optional
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import QueuePool

from ..core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


# Create SQLAlchemy engine with connection pooling
connect_args = {}
if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    connect_args["connect_timeout"] = settings.DB_CONNECT_TIMEOUT

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.POOL_MAX_OVERFLOW,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_recycle=settings.POOL_RECYCLE,
    pool_pre_ping=settings.POOL_PRE_PING,
    echo=settings.SQL_ECHO,
    echo_pool=settings.SQL_ECHO_POOL,
    connect_args=connect_args,
)

# Session factory with scoped sessions for thread safety
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,  # Prevent detached instance errors
    )
)

# Base class for models
Base = declarative_base()

# Import all models to ensure they are registered with SQLAlchemy
# This must be after Base is defined
from ..models import models  # noqa: F401, E402


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields db sessions.
    
    Yields:
        Session: A database session
        
    Example:
        >>> with get_db() as db:
        ...     # use db session
        ...     pass
    """
    db: Optional[Session] = None
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
            db.close()


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Example:
        >>> with db_session() as session:
        ...     # use session
        ...     pass
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Initialize the database by creating all tables."""
    from ..models.base import Base  # noqa: F811
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")


def drop_db() -> None:
    """Drop all database tables."""
    from ..models.base import Base  # noqa: F811
    
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Database tables dropped")


# Optional: Add event listeners for connection tracking
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, params, context, executemany):
    """Log SQL queries for debugging."""
    if settings.SQL_ECHO:
        logger.debug(f"SQL Query: {statement}")


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key constraints for SQLite."""
    if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
