import os
from datetime import timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from pydantic import PostgresDsn, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "Chess Coach API"
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # "postgres" or "sqlite"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "chess_coach"
    DATABASE_URI: Optional[PostgresDsn] = None

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    DB_ECHO: bool = False
    DB_CONNECT_TIMEOUT: int = 5  # seconds

    # Database connection pool
    POOL_SIZE: int = 10
    POOL_MAX_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 30  # seconds
    POOL_RECYCLE: int = 1800  # seconds
    POOL_PRE_PING: bool = True
    
    # SQLAlchemy
    SQL_ECHO: bool = False
    SQL_ECHO_POOL: bool = False
    
    # First Superuser
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None
    
    # External Services
    OPENAI_API_KEY: Optional[str] = None
    
    # Stockfish
    STOCKFISH_PATH: Optional[str] = "stockfish"  # Path to stockfish executable
    STOCKFISH_DEPTH: int = 15
    STOCKFISH_THREADS: int = 4
    STOCKFISH_HASH: int = 128  # MB
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    

    

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Get the SQLAlchemy database URI."""
        if self.DB_TYPE == "sqlite":
            return "sqlite:///./chess_coach.db"

        if self.DATABASE_URI:
            return str(self.DATABASE_URI)
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    @property
    def is_test_environment(self) -> bool:
        """Check if running in test environment."""
        return os.getenv("PYTEST_CURRENT_TEST") is not None or "test" in os.getenv("ENV", "")

# Initialize settings
settings = Settings()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  # React dev server
    "http://localhost:8000",  # FastAPI dev server
    "http://localhost:8080",  # Alternative port
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]

# Update CORS origins from environment variable if set
if settings.BACKEND_CORS_ORIGINS:
    if "*" in settings.BACKEND_CORS_ORIGINS:
        origins = ["*"]
    else:
        # Convert string to list if necessary
        if isinstance(settings.BACKEND_CORS_ORIGINS, str):
            origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]
        else:
            origins = list(settings.BACKEND_CORS_ORIGINS)



# Configure logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": settings.LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                asctime: %(asctime)s
                created: %(created)f
                filename: %(filename)s
                funcName: %(funcName)s
                levelname: %(levelname)s
                levelno: %(levelno)s
                lineno: %(lineno)d
                message: %(message)s
                module: %(module)s
                msec: %(msecs)d
                name: %(name)s
                pathname: %(pathname)s
                process: %(process)d
                processName: %(processName)s
                relativeCreated: %(relativeCreated)d
                thread: %(thread)d
                threadName: %(threadName)s
                exc_info: %(exc_info)s
            """,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": settings.LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": settings.LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": settings.LOG_LEVEL,
            "propagate": True,
        },
        "app": {
            "handlers": ["console", "file"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Apply logging configuration
import logging.config
logging.config.dictConfig(logging_config)

# JWT Configuration
ACCESS_TOKEN_EXPIRE = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

# Security headers
SECURE_HEADERS = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}
