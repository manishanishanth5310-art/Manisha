from app.config import get_settings
from app.models import StoryResponse
from app.services.gemini_client import get_gemini_client


def generate_story(
    outline: list[dict],
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
) -> list[dict]:
    settings = get_settings()
    client = get_gemini_client()

    prompt = f"""
Expand this 5-panel comic outline into polished comic narration and dialogue.

Original idea: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}

Rules:
- Return exactly the same 5 panel numbers and titles.
- Keep the story coherent from panel to panel.
- caption: short ambient/action caption, maximum about 20 words.
- narration: concise comic narration and/or dialogue, maximum about 70 words.
- Do not add markdown.
- Keep image_prompt unchanged unless a small clarity improvement is necessary.
- Avoid offensive, hateful, or unsafe content.

Outline:
{outline}
"""

    try:
        response = client.models.generate_content(
            model=settings["gemini_story_model"],
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": StoryResponse,
            },
        )
    except Exception:
        # A configurable Pro/preview model may not be available for every API key.
        # Fall back to the outline model so the application can still finish.
        response = client.models.generate_content(
            model=settings["gemini_outline_model"],
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": StoryResponse,
            },
        )

    parsed = StoryResponse.model_validate_json(response.text)
    panels = [panel.model_dump() for panel in parsed.panels]

    if len(panels) != 5:
        raise RuntimeError(f"Gemini returned {len(panels)} story panels instead of 5.")

    return panels
