from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@lru_cache
def get_settings():
    return {
        "gemini_api_key": os.getenv("GEMINI_API_KEY", "").strip(),
        "gemini_outline_model": os.getenv("GEMINI_OUTLINE_MODEL", "gemini-3.8-flash").strip(),
        "gemini_story_model": os.getenv("GEMINI_STORY_MODEL", "gemini-3.8-flash").strip(),
        "hf_token": os.getenv("HF_TOKEN", "").strip(),
        "hf_image_model": os.getenv(
            "HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell"
        ).strip(),
        "image_backend": os.getenv("IMAGE_BACKEND", "hf").strip().lower(),
        "local_image_model": os.getenv(
            "LOCAL_IMAGE_MODEL", "runwayml/stable-diffusion-v1-5"
        ).strip(),
        "max_panels": int(os.getenv("MAX_PANELS", "5")),
        "image_width": int(os.getenv("IMAGE_WIDTH", "768")),
        "image_height": int(os.getenv("IMAGE_HEIGHT", "768")),
    }
