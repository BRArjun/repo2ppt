import json
import google.generativeai as genai
from typing import Dict
from app.config import settings
from app.utils.logger import get_logger
from app.prompts.gemini_prompts import SYSTEM_PROMPT, get_analysis_prompt

logger = get_logger(__name__)


class LLMService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        # Configure Gemini with API key
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.generation_config = {
            "temperature": settings.gemini_temperature,
            "max_output_tokens": settings.gemini_max_tokens,
        }
    
    def analyze_codebase(self, digest: str, max_retries: int = 3) -> Dict:
        """
        Analyze codebase digest and generate presentation content
        
        Args:
            digest: Codebase digest content
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dict containing presentation content structure
            
        Raises:
            Exception: If analysis fails after retries
        """
        prompt = get_analysis_prompt(digest)
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Analyzing codebase with Gemini (attempt {attempt + 1}/{max_retries})")
                
                # Generate content
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                # Extract and parse response
                content = response.text.strip()
                
                # Remove markdown code blocks if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                # Parse JSON
                analysis = json.loads(content)
                
                # Validate structure
                required_keys = [
                    "project_name", "tagline", "problem", "solution",
                    "tech_stack", "key_features", "innovation",
                    "architecture", "demo_highlights", "future_scope"
                ]
                
                missing_keys = [key for key in required_keys if key not in analysis]
                if missing_keys:
                    logger.warning(f"Missing keys in response: {missing_keys}")
                    if attempt < max_retries - 1:
                        continue
                    raise Exception(f"Incomplete analysis. Missing: {missing_keys}")
                
                logger.info("Codebase analysis completed successfully")
                return analysis
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info("Retrying with refined prompt...")
                    continue
                raise Exception(f"Failed to get valid JSON from Gemini: {str(e)}")
                
            except Exception as e:
                logger.error(f"Error during analysis: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                    continue
                raise
        
        raise Exception("Failed to analyze codebase after multiple attempts")
    
    def format_for_presenton(self, analysis: Dict) -> str:
        """
        Convert analysis JSON to Presenton content format
        
        Args:
            analysis: Analysis dictionary from Gemini
            
        Returns:
            Formatted content string for Presenton
        """
        content = f"""# {analysis['project_name']}
{analysis['tagline']}

## The Problem
{analysis['problem']}

## Our Solution
{analysis['solution']}

## Tech Stack
{', '.join(analysis['tech_stack'])}

## Key Features
{chr(10).join(f"- {feature}" for feature in analysis['key_features'])}

## Innovation
{analysis['innovation']}

## Architecture
{analysis['architecture']}

## What We'll Demo
{chr(10).join(f"- {item}" for item in analysis['demo_highlights'])}

## Future Roadmap
{chr(10).join(f"- {item}" for item in analysis['future_scope'])}
"""
        return content.strip()