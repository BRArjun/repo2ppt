from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.utils.validators import validate_github_url


class GeneratePresentationRequest(BaseModel):
    """Request model for presentation generation"""
    
    github_url: str = Field(..., description="GitHub repository URL")
    n_slides: Optional[int] = Field(8, ge=5, le=15, description="Number of slides to generate")
    tone: Optional[str] = Field("professional", description="Presentation tone")
    verbosity: Optional[str] = Field("concise", description="Content verbosity")
    language: Optional[str] = Field("English", description="Presentation language")
    template: Optional[str] = Field("general", description="Presentation template")
    export_as: Optional[str] = Field("pptx", description="Export format (pptx or pdf)")
    
    @field_validator('github_url')
    @classmethod
    def validate_url(cls, v):
        is_valid, error_msg = validate_github_url(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @field_validator('tone')
    @classmethod
    def validate_tone(cls, v):
        valid_tones = ["default", "casual", "professional", "funny", "educational", "sales_pitch"]
        if v not in valid_tones:
            raise ValueError(f"Tone must be one of: {', '.join(valid_tones)}")
        return v
    
    @field_validator('verbosity')
    @classmethod
    def validate_verbosity(cls, v):
        valid_verbosity = ["concise", "standard", "text-heavy"]
        if v not in valid_verbosity:
            raise ValueError(f"Verbosity must be one of: {', '.join(valid_verbosity)}")
        return v
    
    @field_validator('export_as')
    @classmethod
    def validate_export(cls, v):
        if v not in ["pptx", "pdf"]:
            raise ValueError("Export format must be 'pptx' or 'pdf'")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "github_url": "https://github.com/admincodes7/zor",
                "n_slides": 8,
                "tone": "professional",
                "verbosity": "concise",
                "language": "English",
                "template": "general",
                "export_as": "pptx"
            }
        }