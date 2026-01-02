import os
from pathlib import Path
import yaml
from typing import Any, Dict, Optional


# Paths
ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config.yaml"


def _load_yaml() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    return {}


def _write_yaml(data: Dict[str, Any]) -> None:
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


class Settings:
    """Simple settings loader that reads env vars first, then falls back to `config.yaml`.

    It exposes a small `update_config` helper to persist presenton/llm/application
    preferences back to `config.yaml` so UI changes can be saved.
    """

    def __init__(self):
        cfg = _load_yaml()

        gem_cfg = cfg.get("gemini", {})
        pres_cfg = cfg.get("presenton", {})
        app_cfg = cfg.get("application", {})

        # Gemini / LLM
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY") or gem_cfg.get("api_key")
        self.gemini_model: str = os.getenv("GEMINI_MODEL") or gem_cfg.get("model", "gemini-2.5-pro")

        # Presenton
        self.presenton_api_key: Optional[str] = os.getenv("PRESENTON_API_KEY") or pres_cfg.get("api_key")
        self.presenton_api_url: str = os.getenv("PRESENTON_API_URL") or pres_cfg.get("api_url", "https://api.presenton.ai")
        self.presenton_tone: str = os.getenv("PRESENTON_TONE") or pres_cfg.get("tone", "professional")
        self.presenton_verbosity: str = os.getenv("PRESENTON_VERBOSITY") or pres_cfg.get("verbosity", "concise")
        self.presenton_template: str = os.getenv("PRESENTON_TEMPLATE") or pres_cfg.get("template", "general")
        self.presenton_include_title_slide: bool = bool(pres_cfg.get("include_title_slide", True))
        self.presenton_include_toc: bool = bool(pres_cfg.get("include_table_of_contents", False))
        self.presenton_export_format: str = pres_cfg.get("export_format", pres_cfg.get("export_as", "pptx"))

        # Application-level
        self.default_slide_count: int = int(os.getenv("DEFAULT_SLIDE_COUNT", app_cfg.get("default_slide_count", 8)))
        self.cleanup_after_generation: bool = bool(os.getenv("CLEANUP_AFTER_GENERATION", app_cfg.get("cleanup_after_generation", True)))

        # Server options
        self.backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
        self.backend_port: int = int(os.getenv("BACKEND_PORT", os.getenv("PORT", 8000)))
        self.debug: bool = bool(os.getenv("DEBUG", False))

    def update_config(self, updates: Dict[str, Any]) -> None:
        """Merge selected settings into `config.yaml` and persist them.

        The function accepts a flat mapping where keys are the attribute names
        of this Settings object (e.g. `presenton_tone`, `presenton_verbosity`,
        `presenton_include_title_slide`, `default_slide_count`). Only a small
        set of keys are persisted (presenton and application settings).
        """
        if not updates:
            return

        cfg = _load_yaml()
        if "presenton" not in cfg:
            cfg["presenton"] = {}
        if "application" not in cfg:
            cfg["application"] = {}

        # Map supported keys into the YAML structure
        mapping = {
            "presenton_tone": ("presenton", "tone"),
            "presenton_verbosity": ("presenton", "verbosity"),
            "presenton_template": ("presenton", "template"),
            "presenton_include_title_slide": ("presenton", "include_title_slide"),
            "presenton_include_toc": ("presenton", "include_table_of_contents"),
            "presenton_export_format": ("presenton", "export_as"),
            "default_slide_count": ("application", "default_slide_count"),
            "cleanup_after_generation": ("application", "cleanup_after_generation"),
        }

        changed = False
        for k, v in updates.items():
            if k in mapping and v is not None:
                section, name = mapping[k]
                # coerce booleans and ints sensibly
                if isinstance(v, bool) or isinstance(v, int) or v is None:
                    cfg.setdefault(section, {})[name] = v
                else:
                    cfg.setdefault(section, {})[name] = v
                setattr(self, k, v)
                changed = True

        if changed:
            _write_yaml(cfg)


# Singleton settings instance used across the app
settings = Settings()
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