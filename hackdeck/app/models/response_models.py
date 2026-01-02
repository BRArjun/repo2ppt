from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PresentationResponse(BaseModel):
    """Response model for successful presentation generation"""
    
    status: str = "success"
    presentation_id: str
    download_url: Optional[str] = None
    edit_url: Optional[str] = None
    credits_consumed: Optional[float] = None
    processing_time: Optional[str] = None
    message: str = "Presentation generated successfully"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "presentation_id": "d3000f96-096c-4768-b67b-e99aed029b57",
                "download_url": "https://...",
                "edit_url": "https://presenton.ai/presentation?id=...",
                "credits_consumed": 50,
                "processing_time": "2.5 minutes",
                "message": "Presentation generated successfully"
            }
        }
    )


class ErrorResponse(BaseModel):
    """Response model for errors"""
    
    status: str = "error"
    error: str
    details: Optional[str] = None
    timestamp: datetime = datetime.now()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "error",
                "error": "Failed to clone repository",
                "details": "Repository not found or is private",
                "timestamp": "2024-01-15T10:30:00"
            }
        }
    )


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: datetime = datetime.now()