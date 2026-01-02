from loguru import logger
import sys
from pathlib import Path
from app.config import settings

# Remove default handler
logger.remove()

# Console handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level,
    colorize=True
)

# File handler
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.add(
    log_dir / "hackdeck_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
    level="DEBUG"
)

# Error file handler
logger.add(
    log_dir / "errors_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
    level="ERROR"
)


def get_logger(name: str):
    """Get a logger instance with the given name"""
    return logger.bind(name=name)