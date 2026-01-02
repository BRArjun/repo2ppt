SYSTEM_PROMPT = """You are a hackathon presentation expert. Analyze codebases and generate concise, impactful presentation content focused on what judges care about."""


def get_analysis_prompt(codebase_digest: str) -> str:
    """Generate the user prompt for codebase analysis"""
    
    return f"""Analyze this codebase and generate presentation content for a hackathon project.

CODEBASE STRUCTURE AND CONTENT:
{codebase_digest}

INSTRUCTIONS:
Generate a JSON response with the following structure. Be concise and focus ONLY on what matters for a hackathon presentation.

Required sections:
1. project_name: Extract or infer the project name
2. tagline: One sentence that captures the essence (max 10 words)
3. problem: What problem does this solve? (2-3 sentences)
4. solution: How does this project solve it? (2-3 sentences)
5. tech_stack: List main technologies used (frameworks, languages, key libraries)
6. key_features: 3-5 bullet points of main features
7. innovation: What makes this unique or innovative? (2-3 sentences)
8. architecture: Brief overview of system design (2-3 sentences)
9. demo_highlights: What should be demonstrated? (2-3 points)
10. future_scope: Potential improvements or next steps (2-3 points)

GUIDELINES:
- Be specific, not generic
- Focus on impact and innovation
- Use active voice
- Avoid jargon unless necessary
- Highlight technical achievements
- Keep it exciting but honest

OUTPUT FORMAT: Valid JSON only, no markdown formatting or code blocks.

Example output structure:
{{
  "project_name": "ProjectName",
  "tagline": "Brief catchy description",
  "problem": "Clear problem statement",
  "solution": "How the project addresses it",
  "tech_stack": ["Python", "React", "PostgreSQL"],
  "key_features": ["Feature 1", "Feature 2", "Feature 3"],
  "innovation": "What sets this apart",
  "architecture": "System design overview",
  "demo_highlights": ["Demo point 1", "Demo point 2"],
  "future_scope": ["Future improvement 1", "Future improvement 2"]
}}"""


PRESENTON_INSTRUCTIONS = """Create a modern, visually engaging hackathon presentation.
- Use bold colors and clean layouts
- Include relevant icons where appropriate
- Keep text minimal and impactful
- Focus on visual hierarchy
- Make it demo-ready
"""