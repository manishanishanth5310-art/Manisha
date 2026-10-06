from app.config import get_settings
from app.models import OutlineResponse
from app.services.gemini_client import get_gemini_client


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> list[dict]:
    settings = get_settings()
    client = get_gemini_client()

    prompt = f"""
Create a cohesive 5-panel comic outline.

User story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Requirements:
- Exactly 5 panels.
- Keep the same main character and visual identity across all panels.
- Make the story have a clear beginning, development, turning point, and ending.
- scene_description should describe visible action, environment, lighting, and emotion.
- image_prompt should be suitable for a text-to-image model.
- Do not put speech bubbles or written words inside image_prompt.
- Keep image_prompt visually specific and consistent.
"""

    response = client.models.generate_content(
        model=settings["gemini_outline_model"],
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": OutlineResponse,
        },
    )

    parsed = OutlineResponse.model_validate_json(response.text)
    panels = [panel.model_dump() for panel in parsed.panels]

    if len(panels) != 5:
        raise RuntimeError(f"Gemini returned {len(panels)} panels instead of 5.")

    return panels
