import streamlit as st
import requests
import time
from typing import Dict, Any, Optional
import pandas as pd
import altair as alt
from datetime import datetime

# =========================================================
# PAGE CONFIG (FORCE DARK MODE)
# =========================================================
st.set_page_config(
    page_title="HackDeck",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# =========================================================
# SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================================================
# DARK THEMES ONLY
# =========================================================
THEMES = {
    "professional-dark": {
        "primary": "#3B82F6",
        "secondary": "#60A5FA",
        "bg": "#0B0F19",
        "card": "#111827",
        "border": "#1F2937",
        "text": "#E5E7EB",
        "muted": "#9CA3AF",
        "heading": "#F9FAFB"
    },
    "edge-yellow": {
        "primary": "#FACC15",
        "secondary": "#FDE68A",
        "bg": "#0A0A0A",
        "card": "#121212",
        "border": "#1F1F1F",
        "text": "#EAEAEA",
        "muted": "#9CA3AF",
        "heading": "#FACC15"
    },
    "mint-blue": {
        "primary": "#2DD4BF",
        "secondary": "#38BDF8",
        "bg": "#020617",
        "card": "#020617",
        "border": "#0F172A",
        "text": "#CBD5E1",
        "muted": "#94A3B8",
        "heading": "#E0F2FE"
    }
}

# =========================================================
# THEME + DARK OVERRIDES
# =========================================================
def apply_dark_theme(theme: Dict[str, str]):
    st.markdown(f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background-color: {theme['bg']} !important;
        color: {theme['text']} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {theme['card']} !important;
        border-right: 1px solid {theme['border']};
    }}

    h1, h2, h3, h4 {{
        color: {theme['heading']} !important;
    }}

    .card {{
        background: {theme['card']};
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid {theme['border']};
        margin-bottom: 1.5rem;
        animation: fadeUp 0.4s ease;
    }}

    .action-card {{
        background: linear-gradient(135deg, {theme['card']}, {theme['bg']});
        border-radius: 14px;
        padding: 1.25rem;
        border: 1px solid {theme['border']};
    }}

    input, textarea {{
        background-color: {theme['bg']} !important;
        color: {theme['text']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 10px !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: {theme['bg']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 10px !important;
    }}

    div[data-baseweb="select"] span {{
        color: {theme['text']} !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
        color: #020617 !important;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# API CALL
# =========================================================
def generate_presentation(payload: Dict[str, Any]) -> Optional[dict]:
    try:
        response = requests.post(
            f"{API_URL}/api/v1/generate",
            json=payload,
            timeout=300
        )
        if response.status_code == 200:
            return response.json()
        st.error(response.json().get("detail", "Generation failed"))
    except requests.exceptions.Timeout:
        st.error("Request timed out")
    return None

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.title("🎨 HackDeck")

    theme_name = st.selectbox("Theme", list(THEMES.keys()), index=0)
    apply_dark_theme(THEMES[theme_name])

    st.markdown("---")
    page = st.radio("Navigation", ["Generator", "Dashboard"])

# =========================================================
# GENERATOR PAGE
# =========================================================
if page == "Generator":
    st.title("🚀 Hackathon Presentation Generator")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        github_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repo"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            n_slides = st.slider("Number of Slides", 5, 50, 8)
            tone = st.selectbox(
                "Tone",
                ["default", "casual", "professional", "funny", "educational", "sales_pitch"]
            )

        with col2:
            verbosity = st.selectbox("Verbosity", ["concise", "standard", "text-heavy"])
            language = st.text_input("Language", "English")

        with col3:
            image_type = st.selectbox("Image Type", ["stock", "ai-generated"])
            export_as = st.selectbox("Export Format", ["pptx", "pdf"])

        st.markdown("### ⚙️ Options")
        c1, c2, c3 = st.columns(3)
        include_title = c1.toggle("Include Title Slide", True)
        # include_toc = c2.toggle("Include Table of Contents", False)
        # web_search = c3.toggle("Enable Web Search", False)

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ Generate Presentation"):
        if not github_url.startswith("https://github.com/"):
            st.error("Please enter a valid GitHub repository URL")
        else:
            start_time = time.time()
            with st.spinner("Generating presentation..."):
                result = generate_presentation({
                    "github_url": github_url,
                    "n_slides": n_slides,
                    "tone": tone,
                    "verbosity": verbosity,
                    "language": language,
                    "image_type": image_type,
                    "export_as": export_as,
                    "include_title_slide": include_title,
                    # "include_table_of_contents": include_toc,
                    # "web_search": web_search,
                    "theme": theme_name
                })

            if result:
                duration = round(time.time() - start_time, 2)

                st.success("🎉 Presentation generated successfully")
                st.metric("⏱ Processing Time (s)", duration)

                st.markdown("### 📂 Your Presentation")
                with st.container():
                    st.markdown('<div class="action-card">', unsafe_allow_html=True)

                    if result.get("edit_url"):
                        st.markdown(
                            f"👀 **[View / Edit Presentation]({result['edit_url']})**",
                            unsafe_allow_html=True
                        )

                    if result.get("download_url"):
                        st.markdown(
                            f"⬇️ **[Download Presentation]({result['download_url']})**",
                            unsafe_allow_html=True
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

                st.session_state.history.append({
                    "time": datetime.now(),
                    "slides": n_slides,
                    "tone": tone,
                    "format": export_as,
                    "duration": duration
                })

# =========================================================
# DASHBOARD
# =========================================================
else:
    st.title("📊 Dashboard")

    if not st.session_state.history:
        st.info("No presentations generated yet.")
    else:
        df = pd.DataFrame(st.session_state.history)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Decks", len(df))
        col2.metric("Avg Slides", round(df["slides"].mean(), 1))
        col3.metric("Avg Time (s)", round(df["duration"].mean(), 2))

        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x="time:T",
                y="duration:Q",
                tooltip=["slides", "tone", "format"]
            )
            .properties(height=300)
        )

        st.altair_chart(chart, use_container_width=True)
        st.dataframe(df.sort_values("time", ascending=False), use_container_width=True)
# =========================================================