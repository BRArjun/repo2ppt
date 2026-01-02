import re
import validators as validator_lib
from urllib.parse import urlparse


def validate_github_url(url: str) -> tuple[bool, str]:
    """
    Validate if the URL is a valid GitHub repository URL
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"
    
    # Basic URL validation
    if not validator_lib.url(url):
        return False, "Invalid URL format"
    
    # Parse URL
    parsed = urlparse(url)
    
    # Check if it's GitHub
    if parsed.netloc not in ["github.com", "www.github.com"]:
        return False, "URL must be from github.com"
    
    # GitHub repo URL pattern: /username/repository
    path_pattern = r'^/[\w-]+/[\w.-]+/?$'
    if not re.match(path_pattern, parsed.path):
        return False, "Invalid GitHub repository URL format. Expected: https://github.com/username/repository"
    
    return True, ""


def extract_repo_info(url: str) -> dict:
    """
    Extract repository owner and name from GitHub URL
    
    Returns:
        dict: {"owner": str, "repo": str, "full_name": str}
    """
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split('/') if p]
    
    if len(path_parts) >= 2:
        return {
            "owner": path_parts[0],
            "repo": path_parts[1].replace('.git', ''),
            "full_name": f"{path_parts[0]}/{path_parts[1].replace('.git', '')}"
        }
    
    return {"owner": "", "repo": "", "full_name": ""}


def sanitize_repo_name(name: str) -> str:
    """Sanitize repository name for use as directory name"""
    return re.sub(r'[^\w\-.]', '_', name)