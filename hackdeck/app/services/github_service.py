import git
import shutil
from pathlib import Path
from typing import Optional
from app.config import settings
from app.utils.logger import get_logger
from app.utils.validators import extract_repo_info, sanitize_repo_name

logger = get_logger(__name__)


class GitHubService:
    """Service for handling GitHub repository operations"""
    
    def __init__(self):
        self.temp_dir = Path(settings.temp_repo_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def clone_repository(self, github_url: str) -> Path:
        """
        Clone a GitHub repository to local temp directory
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Path to cloned repository
            
        Raises:
            Exception: If cloning fails
        """
        try:
            # Extract repo info
            repo_info = extract_repo_info(github_url)
            repo_name = sanitize_repo_name(repo_info['repo'])
            
            # Create unique directory path
            clone_path = self.temp_dir / f"{repo_info['owner']}_{repo_name}"
            
            # Remove if already exists
            if clone_path.exists():
                logger.info(f"Removing existing directory: {clone_path}")
                shutil.rmtree(clone_path)
            
            logger.info(f"Cloning repository: {github_url}")
            
            # Clone repository (shallow clone for speed)
            git.Repo.clone_from(
                github_url,
                clone_path,
                depth=1,  # Only get latest commit
                single_branch=True  # Only default branch
            )
            
            logger.info(f"Repository cloned successfully to: {clone_path}")
            
            # Check size
            size_mb = self._get_directory_size(clone_path)
            if size_mb > settings.max_repo_size_mb:
                self.cleanup_repository(clone_path)
                raise Exception(f"Repository size ({size_mb}MB) exceeds maximum allowed ({settings.max_repo_size_mb}MB)")
            
            return clone_path
            
        except git.exc.GitCommandError as e:
            logger.error(f"Git clone failed: {str(e)}")
            raise Exception(f"Failed to clone repository. It may be private or doesn't exist: {str(e)}")
        except Exception as e:
            logger.error(f"Error cloning repository: {str(e)}")
            raise
    
    def cleanup_repository(self, repo_path: Path) -> None:
        """
        Delete cloned repository from temp directory
        
        Args:
            repo_path: Path to repository to delete
        """
        try:
            if repo_path.exists():
                logger.info(f"Cleaning up repository: {repo_path}")
                shutil.rmtree(repo_path)
                logger.info("Repository cleaned up successfully")
        except Exception as e:
            logger.error(f"Error cleaning up repository: {str(e)}")
    
    def _get_directory_size(self, path: Path) -> float:
        """
        Calculate directory size in MB
        
        Args:
            path: Directory path
            
        Returns:
            Size in MB
        """
        total_size = 0
        for item in path.rglob('*'):
            if item.is_file():
                total_size += item.stat().st_size
        return total_size / (1024 * 1024)  # Convert to MB