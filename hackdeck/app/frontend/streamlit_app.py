import streamlit as st
import requests
from typing import Optional

# Page config
st.set_page_config(
    page_title="HackDeck - Hackathon Presentation Generator",
    page_icon="🚀",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .success-box {
        padding: 1.5rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        padding: 1.5rem;
        background-color: #f8d7da;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if backend API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def generate_presentation(
    github_url: str,
    n_slides: int,
    tone: str,
    verbosity: str,
    language: str,
    template: str,
    export_as: str
) -> Optional[dict]:
    """Call API to generate presentation"""
    try:
        payload = {
            "github_url": github_url,
            "n_slides": n_slides,
            "tone": tone,
            "verbosity": verbosity,
            "language": language,
            "template": template,
            "export_as": export_as
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/generate",
            json=payload,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            st.error(f"Error: {error_data.get('detail', 'Unknown error')}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. The repository might be too large.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# Main UI
def main():
    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🚀 HackDeck")
    st.subheader("Automated Presentation Generator for Hackathon Projects")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ Backend API is not running. Please start the FastAPI server.")
        st.code("uvicorn app.main:app --reload", language="bash")
        return
    
    st.success("✅ Backend API is running")
    st.markdown("---")
    
    # Instructions
    with st.expander("ℹ️ How to use HackDeck", expanded=False):
        st.markdown("""
        1. **Enter your GitHub repository URL** (must be public)
        2. **Configure presentation options** (or use defaults)
        3. **Click Generate** and wait 2-3 minutes
        4. **Download or edit** your presentation!
        
        **Note:** Your repository will be temporarily cloned and automatically deleted after processing.
        """)
    
    # Main form
    st.markdown("### 📝 Repository Details")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        github_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter the URL of your public GitHub repository"
        )
    
    with col2:
        n_slides = st.slider(
            "Number of Slides",
            min_value=5,
            max_value=15,
            value=8,
            help="Total number of slides to generate"
        )
    
    # Advanced options
    with st.expander("⚙️ Advanced Options", expanded=False):
        col3, col4 = st.columns(2)
        
        with col3:
            tone = st.selectbox(
                "Presentation Tone",
                ["professional", "casual", "educational", "sales_pitch", "funny"],
                index=0
            )
            
            verbosity = st.selectbox(
                "Content Verbosity",
                ["concise", "standard", "text-heavy"],
                index=0,
                help="How detailed should the content be?"
            )
            
            language = st.text_input(
                "Language",
                value="English"
            )
        
        with col4:
            template = st.selectbox(
                "Template",
                ["general", "modern", "standard", "swift"],
                index=0
            )
            
            export_as = st.selectbox(
                "Export Format",
                ["pptx", "pdf"],
                index=0
            )
    
    st.markdown("---")
    
    # Generate button
    if st.button("🎨 Generate Presentation", type="primary"):
        if not github_url:
            st.error("Please enter a GitHub repository URL")
            return
        
        if not github_url.startswith("https://github.com/"):
            st.error("Please enter a valid GitHub URL (must start with https://github.com/)")
            return
        
        # Show progress
        with st.spinner("🔄 Generating your presentation... This may take 2-3 minutes"):
            # Progress steps
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            progress_text.text("Step 1/5: Cloning repository...")
            progress_bar.progress(20)
            
            # Call API
            result = generate_presentation(
                github_url=github_url,
                n_slides=n_slides,
                tone=tone,
                verbosity=verbosity,
                language=language,
                template=template,
                export_as=export_as
            )
            
            progress_bar.progress(100)
            progress_text.empty()
            progress_bar.empty()
            
            if result:
                # Success
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Presentation generated successfully!")
                
                col5, col6, col7 = st.columns(3)
                
                with col5:
                    st.metric("Presentation ID", result.get("presentation_id", "N/A")[:20] + "...")
                
                with col6:
                    st.metric("Processing Time", result.get("processing_time", "N/A"))
                
                with col7:
                    st.metric("Credits Used", result.get("credits_consumed", "N/A"))
                
                st.markdown("---")
                
                # Download and edit links
                if result.get("edit_url"):
                    st.markdown(f"🔗 **[Edit Online]({result['edit_url']})**")
                
                if result.get("download_url"):
                    st.info(f"📥 Download path: `{result['download_url']}`")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Made with ❤️ for hackathon participants | "
        "<a href='https://github.com/yourusername/hackdeck'>GitHub</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()