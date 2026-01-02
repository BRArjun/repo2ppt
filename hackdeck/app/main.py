from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import time
from app.config import settings
from app.models.request_models import GeneratePresentationRequest
from app.models.response_models import (
    PresentationResponse,
    ErrorResponse,
    HealthResponse
)
from app.services.github_service import GitHubService
from app.services.digest_service import DigestService
from app.services.llm_service import LLMService
from app.services.presenton_service import PresentonService
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="HackDeck API",
    description="Automated Presentation Generator for Hackathon Projects",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GitHubService()
digest_service = DigestService()
llm_service = LLMService()
presenton_service = PresentonService()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to HackDeck API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now()
    )


@app.post(
    "/api/v1/generate",
    response_model=PresentationResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    tags=["Presentation"]
)
async def generate_presentation(request: GeneratePresentationRequest):
    """
    Generate a presentation from a GitHub repository
    
    - **github_url**: GitHub repository URL
    - **n_slides**: Number of slides to generate (5-15)
    - **tone**: Presentation tone (professional, casual, etc.)
    - **verbosity**: Content verbosity (concise, standard, text-heavy)
    - **language**: Presentation language
    - **template**: Presentation template
    - **export_as**: Export format (pptx or pdf)
    """
    start_time = time.time()
    repo_path = None
    
    try:
        logger.info(f"Starting presentation generation for: {request.github_url}")
        # Persist user's UI preferences into config.yaml so changes survive
        try:
            settings.update_config({
                "presenton_tone": request.tone,
                "presenton_verbosity": request.verbosity,
                "presenton_template": request.template,
                "presenton_export_format": request.export_as,
                "presenton_include_title_slide": getattr(request, "include_title_slide", None),
                "presenton_include_toc": getattr(request, "include_table_of_contents", None),
                "default_slide_count": request.n_slides
            })
        except Exception:
            # non-fatal: persist best-effort
            logger.debug("Failed to persist UI preferences to config.yaml")
        
        # Step 1: Clone repository
        logger.info("Step 1/5: Cloning repository...")
        repo_path = github_service.clone_repository(request.github_url)
        
        # Step 2: Generate digest
        logger.info("Step 2/5: Analyzing codebase...")
        digest = digest_service.generate_digest(repo_path)
        digest = digest_service.summarize_digest(digest)
        
        # Step 3: Analyze with LLM
        logger.info("Step 3/5: Generating content with AI...")
        analysis = llm_service.analyze_codebase(digest)
        
        # Step 4: Format content for Presenton
        logger.info("Step 4/5: Formatting presentation content...")
        content = llm_service.format_for_presenton(analysis)
        
        # Step 5: Generate presentation
        logger.info("Step 5/5: Creating presentation...")
        presenton_result = presenton_service.generate_presentation(
            content=content,
            n_slides=request.n_slides,
            tone=request.tone,
            verbosity=request.verbosity,
            language=request.language,
            template=request.template,
            export_as=request.export_as
            , include_title_slide=getattr(request, "include_title_slide", None)
            , include_table_of_contents=getattr(request, "include_table_of_contents", None)
            , web_search=getattr(request, "web_search", None)
            , image_type=getattr(request, "image_type", None)
        )
        
        # Cleanup
        if settings.cleanup_after_generation and repo_path:
            github_service.cleanup_repository(repo_path)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        processing_time_str = f"{processing_time:.1f} seconds"
        
        logger.info(f"Presentation generated successfully in {processing_time_str}")
        
        # Return response
        return PresentationResponse(
            status="success",
            presentation_id=presenton_result.get("presentation_id"),
            download_url=presenton_result.get("path"),
            edit_url=presenton_result.get("edit_path"),
            credits_consumed=presenton_result.get("credits_consumed"),
            processing_time=processing_time_str,
            message="Presentation generated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error generating presentation: {str(e)}")
        
        # Cleanup on error
        if repo_path:
            try:
                github_service.cleanup_repository(repo_path)
            except:
                pass
        
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug
    )