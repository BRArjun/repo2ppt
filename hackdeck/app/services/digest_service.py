import subprocess
from pathlib import Path
from typing import Optional
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DigestService:
    """Service for generating codebase digests using codebase-digest tool"""
    
    def __init__(self):
        self.ignore_patterns = settings.digest_ignore_patterns
    
    def generate_digest(self, repo_path: Path) -> str:
        """
        Generate codebase digest for a repository
        
        Args:
            repo_path: Path to cloned repository
            
        Returns:
            Digest content as string
            
        Raises:
            Exception: If digest generation fails
        """
        try:
            logger.info(f"Generating digest for repository: {repo_path}")
            
            # Get repo name for output file
            repo_name = repo_path.name
            output_file = Path(f"{repo_name}_codebase_digest.md")
            
            # Build cdigest command with file output
            cmd = [
                "cdigest",
                str(repo_path),
                "-d", str(settings.digest_max_depth),
                "-o", settings.digest_output_format,
                "-f", str(output_file),  # Output to file
                "--max-size", "10240"  # 10MB max per file
            ]
            
            # Add ignore patterns
            if self.ignore_patterns:
                cmd.extend(["--ignore"] + self.ignore_patterns)
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            # Execute command with stdin closed to prevent interactive prompts
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                stdin=subprocess.DEVNULL  # Prevent interactive prompts
            )
            
            # Check if output file was created
            if output_file.exists():
                logger.info(f"Reading digest from file: {output_file}")
                digest_content = output_file.read_text()
                
                # Clean up the output file
                output_file.unlink()
                
                logger.info(f"Digest generated successfully. Length: {len(digest_content)} characters")
                
                # Validate output
                if not digest_content or len(digest_content) < 100:
                    raise Exception("Generated digest is too short or empty")
                
                return digest_content
            else:
                logger.error(f"Digest generation failed with return code: {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                raise Exception(f"Output file not created. Return code: {result.returncode}")
            
            return digest_content
            
        except subprocess.TimeoutExpired:
            logger.error("Digest generation timed out")
            raise Exception("Digest generation took too long. Repository may be too large.")
        except Exception as e:
            logger.error(f"Error generating digest: {str(e)}")
            raise
    
    def summarize_digest(self, digest: str, max_length: int = 50000) -> str:
        """
        Truncate digest if it's too long for LLM context
        
        Args:
            digest: Full digest content
            max_length: Maximum character length
            
        Returns:
            Truncated or full digest
        """
        if len(digest) <= max_length:
            return digest
        
        logger.warning(f"Digest too long ({len(digest)} chars). Truncating to {max_length}")
        
        # Keep the directory structure and truncate file contents
        truncated = digest[:max_length]
        truncated += "\n\n... [Content truncated due to size limits] ..."
        
        return truncated