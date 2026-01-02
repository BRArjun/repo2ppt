import requests
from typing import Dict, Optional
from app.config import settings
from app.utils.logger import get_logger
from app.prompts.gemini_prompts import PRESENTON_INSTRUCTIONS

logger = get_logger(__name__)


class PresentonService:
    """Service for interacting with Presenton API"""
    
    def __init__(self):
        self.api_url = settings.presenton_api_url
        self.api_key = settings.presenton_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_presentation(
        self,
        content: str,
        n_slides: int = None,
        tone: str = None,
        verbosity: str = None,
        language: str = "English",
        template: str = None,
        export_as: str = None,
        include_title_slide: Optional[bool] = None,
        include_table_of_contents: Optional[bool] = None,
        web_search: Optional[bool] = None,
        image_type: Optional[str] = None,
    ) -> Dict:
        """
        Generate presentation using Presenton API
        
        Args:
            content: Presentation content
            n_slides: Number of slides
            tone: Presentation tone
            verbosity: Content verbosity
            language: Presentation language
            template: Template name
            export_as: Export format
            
        Returns:
            Dict containing presentation_id, path, edit_path, credits_consumed
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Use defaults from settings if not provided
            n_slides = n_slides or settings.default_slide_count
            tone = tone or settings.presenton_tone
            verbosity = verbosity or settings.presenton_verbosity
            template = template or settings.presenton_template
            export_as = export_as or settings.presenton_export_format
            include_title_slide = include_title_slide if include_title_slide is not None else settings.presenton_include_title_slide
            include_table_of_contents = include_table_of_contents if include_table_of_contents is not None else settings.presenton_include_toc
            web_search = web_search if web_search is not None else False
            image_type = image_type or "stock"
            
            logger.info(f"Generating presentation with {n_slides} slides")
            
            # Prepare request payload
            payload = {
                "content": content,
                "instructions": PRESENTON_INSTRUCTIONS,
                "tone": tone,
                "verbosity": verbosity,
                "n_slides": n_slides,
                "language": language,
                "template": template,
                "include_title_slide": include_title_slide,
                "include_table_of_contents": include_table_of_contents,
                "export_as": export_as,
                "markdown_emphasis": True,
                "web_search": web_search,
                "image_type": image_type
            }
            
            # Make API request
            endpoint = f"{self.api_url}/api/v1/ppt/presentation/generate"
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=180  # 3 minute timeout
            )
            
            # Check response
            if response.status_code != 200:
                error_detail = response.json() if response.text else "No error details"
                logger.error(f"Presenton API error: {response.status_code} - {error_detail}")
                raise Exception(f"Failed to generate presentation: {error_detail}")
            
            result = response.json()
            
            logger.info(f"Presentation generated successfully. ID: {result.get('presentation_id')}")
            
            return result
            
        except requests.exceptions.Timeout:
            logger.error("Presenton API request timed out")
            raise Exception("Presentation generation timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Presenton API request failed: {str(e)}")
            raise Exception(f"Failed to connect to Presenton API: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating presentation: {str(e)}")
            raise
    
    def export_presentation(
        self,
        presentation_id: str,
        export_as: str = "pptx"
    ) -> Dict:
        """
        Export existing presentation in different format
        
        Args:
            presentation_id: ID of the presentation
            export_as: Export format (pptx or pdf)
            
        Returns:
            Dict containing presentation details
        """
        try:
            logger.info(f"Exporting presentation {presentation_id} as {export_as}")
            
            payload = {
                "id": presentation_id,
                "export_as": export_as
            }
            
            endpoint = f"{self.api_url}/api/v1/ppt/presentation/export"
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=120
            )
            
            if response.status_code != 200:
                error_detail = response.json() if response.text else "No error details"
                raise Exception(f"Failed to export presentation: {error_detail}")
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error exporting presentation: {str(e)}")
            raise