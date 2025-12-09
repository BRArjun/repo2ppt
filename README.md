# repo2ppt 

**Automated Presentation Generator for Hackathon Projects**

repo2ppt helps hackathon participants automatically generate professional presentations from their GitHub repositories, so they can focus on building rather than creating slides.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Problem Statement

Hackathon participants often spend valuable time creating presentations instead of focusing on their core product. They need a quick way to generate professional-looking slides that showcase their project effectively.

---

## Solution

repo2ppt automatically:
1. Analyzes your GitHub repository
2. Understands your project structure and purpose
3. Generates a focused, hackathon-ready presentation
4. Delivers a downloadable/editable PowerPoint file

All with just a GitHub link!

---

## ✨ Features

- **One-Click Generation**: Just paste your GitHub repo link
- **Intelligent Analysis**: Uses LLM to understand your codebase
- **Hackathon-Focused**: Generates only essential slides (no fluff)
- **Credit-Efficient**: Optimized to minimize API costs
- **Quick Turnaround**: Get your presentation in minutes
- **Customizable Output**: Control slide count, tone, and format
- **Clean Output**: Excludes config files, env files, and unnecessary content

---

## 🛠 Tech Stack

### Frontend
- **Streamlit** - Simple, fast web interface

### Backend
- **FastAPI** - High-performance REST API
- **Python 3.9+** - Core language

### Code Analysis
- **codebase-digest** - Repository analysis and content extraction

### AI/LLM
- **Claude API** (Anthropic) or **OpenAI API** - Intelligent content generation

### Presentation Generation
- **Presenton API** - Professional slide deck creation

### Other Tools
- **GitPython** - Repository cloning
- **Python-dotenv** - Environment management
- **Requests** - HTTP client

---

## 🏗 Architecture

### System Components

```
┌─────────────────┐
│  Streamlit UI   │  ← User Interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │  ← Business Logic
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬───────────┐
    │         │          │           │
    ▼         ▼          ▼           ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌──────────┐
│GitHub  │ │Code  │ │  LLM   │ │Presenton │
│Clone   │ │Digest│ │  API   │ │   API    │
└────────┘ └──────┘ └────────┘ └──────────┘
```

### Data Flow

1. **Input**: User submits GitHub URL
2. **Clone**: Repository cloned to temporary directory
3. **Analyze**: Codebase-digest scans all core files
4. **Generate**: LLM analyzes digest and creates presentation content
5. **Format**: Content structured for Presenton API
6. **Create**: Presenton generates the presentation
7. **Deliver**: User receives download/edit links
8. **Cleanup**: Temporary files deleted

---

## Installation

### Prerequisites

- Python 3.9 or higher
- Git installed on your system
- API keys for:
  - LLM service (Claude or OpenAI)
  - Presenton API

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/repo2ppt.git
cd repo2ppt
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Codebase Digest

```bash
pip install codebase-digest
```

---

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# LLM API Configuration (Choose one)
ANTHROPIC_API_KEY=your_claude_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here

# Presenton API
PRESENTON_API_KEY=your_presenton_api_key_here
PRESENTON_API_URL=https://api.presenton.ai

# Application Settings
TEMP_REPO_DIR=./temp_repos
MAX_REPO_SIZE_MB=500
DEFAULT_SLIDE_COUNT=8
CLEANUP_AFTER_GENERATION=true

# Optional: Caching
ENABLE_DIGEST_CACHE=false
CACHE_EXPIRY_HOURS=24
```

### Configuration File

Optionally create `config.yaml`:

```yaml
codebase_digest:
  max_depth: 10
  output_format: "markdown"
  show_size: false
  ignore_patterns:
    - "*.pyc"
    - "*.log"
    - "node_modules"
    - ".venv"
    - ".env"
    - "*.config"
    - "package-lock.json"
    - "yarn.lock"

llm:
  model: "claude-sonnet-4-20250514"  # or "gpt-4"
  max_tokens: 4000
  temperature: 0.7

presenton:
  tone: "professional"
  verbosity: "concise"
  template: "general"
  include_title_slide: true
  include_table_of_contents: false
  export_as: "pptx"
```

---

## Usage

### Running the Application

#### 1. Start the Backend (FastAPI)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Start the Frontend (Streamlit)

In a new terminal:

```bash
streamlit run app/frontend/streamlit_app.py
```

#### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

### Using repo2ppt

1. **Enter GitHub URL**: Paste your repository link
2. **Configure Options** (Optional):
   - Number of slides (default: 8)
   - Presentation tone (professional/casual/educational)
   - Verbosity (concise/standard)
3. **Generate**: Click "Generate Presentation"
4. **Wait**: Processing typically takes 1-3 minutes
5. **Download**: Get your presentation file or edit online

---

## Project Structure

```
repo2ppt/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py   # Pydantic request models
│   │   └── response_models.py  # Pydantic response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github_service.py   # GitHub cloning logic
│   │   ├── digest_service.py   # Codebase digest integration
│   │   ├── llm_service.py      # LLM API integration
│   │   ├── presenton_service.py# Presenton API integration
│   │   └── file_manager.py     # Temp file management
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py       # URL and input validation
│   │   ├── logger.py           # Logging configuration
│   │   └── helpers.py          # Helper functions
│   └── frontend/
│       └── streamlit_app.py    # Streamlit UI
├── temp_repos/                  # Temporary clone directory (gitignored)
├── tests/
│   ├── __init__.py
│   ├── test_github_service.py
│   ├── test_digest_service.py
│   └── test_llm_service.py
├── .env.example                 # Example environment variables
├── .gitignore
├── requirements.txt
├── config.yaml
├── README.md
└── LICENSE
```

---

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Debug Mode

Set environment variable:
```bash
export DEBUG=true
```

---

## Security Considerations

- Never commit `.env` file with API keys
- Validate all GitHub URLs to prevent malicious inputs
- Limit repository size to prevent resource exhaustion
- Implement rate limiting on API endpoints
- Clean up temporary files after processing
- Use secure temporary directory creation

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Authors

- **B R Arjun** - Initial work - [@GitKraken](https://github.com/BRArjun)

---

## Acknowledgments

- [codebase-digest](https://github.com/kamilstanuch/codebase-digest) - For code analysis
- [Presenton API](https://presenton.ai) - For presentation generation

---
