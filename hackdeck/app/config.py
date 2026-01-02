from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Google Gemini
    google_api_key: str = ""
    gemini_model: str = "gemini-pro"
    
    # Presenton API
    presenton_api_key: str = ""
    presenton_api_url: str = "https://api.presenton.ai"
    
    # Application
    temp_repo_dir: Path = Path("./temp_repos")
    max_repo_size_mb: int = 500
    default_slide_count: int = 8
    cleanup_after_generation: bool = True
    log_level: str = "INFO"
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 8501
    
    # Caching
    enable_digest_cache: bool = False
    cache_expiry_hours: int = 24
    
    # Development
    debug: bool = False
    
    # Codebase Digest Config
    digest_max_depth: int = 10
    digest_output_format: str = "markdown"
    digest_ignore_patterns: list = [
        "*.pyc", "*.pyo", "*.pyd", "__pycache__",
        "node_modules", "bower_components",
        ".git", ".svn", ".hg", ".gitignore",
        "venv", ".venv", "env", ".env", "*.env",
        ".idea", ".vscode",
        "*.log", "*.bak", "*.swp", "*.tmp",
        ".DS_Store", "Thumbs.db",
        "build", "dist",
        ".egg-info",
        "*.so", "*.dylib", "*.dll",
        "package-lock.json", "yarn.lock", "poetry.lock",
        "*.config.js", "*.config.ts"
    ]
    
    # Gemini Settings
    gemini_temperature: float = 0.7
    gemini_max_tokens: int = 4000
    
    # Presenton Settings
    presenton_tone: str = "professional"
    presenton_verbosity: str = "concise"
    presenton_template: str = "general"
    presenton_include_title_slide: bool = True
    presenton_include_toc: bool = False
    presenton_export_format: str = "pptx"
    
    
# Global settings instance
settings = Settings()