"""File management utilities"""

from pathlib import Path
import shutil
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FileManager:
    """Service for managing temporary files and directories"""
    
    @staticmethod
    def cleanup_directory(directory: Path) -> None:
        """
        Clean up a directory and all its contents
        
        Args:
            directory: Path to directory to clean
        """
        try:
            if directory.exists() and directory.is_dir():
                shutil.rmtree(directory)
                logger.info(f"Cleaned up directory: {directory}")
        except Exception as e:
            logger.error(f"Error cleaning directory {directory}: {str(e)}")
    
    @staticmethod
    def ensure_directory(directory: Path) -> None:
        """
        Ensure directory exists, create if it doesn't
        
        Args:
            directory: Path to directory
        """
        directory.mkdir(parents=True, exist_ok=True)