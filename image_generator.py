from pathlib import Path
import re
import uuid

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings

BASE_DIR = Path(__file__).resolve().parents[2]
PANELS_DIR = BASE_DIR / "static" / "panels"


def _safe_name(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", text).strip("-").lower()
    return value[:50] or "panel"


def _placeholder_image(prompt: str, output_path: Path, width: int, height: int) -> None:
    # Local fallback so the application remains testable even without an image API.
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, width - 20, height - 20), outline="black", width=4)
    draw.text((40, 45), "ComicCraft", fill="black")
    draw.text((40, 90), "Image generation unavailable", fill="black")
    words = prompt.split()
    lines = []
    line = ""
    for word in words[:45]:
        if len(line) + len(word) + 1 > 42:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    y = 150
    for text in lines:
        draw.text((40, y), text, fill="black")
        y += 24
    image.save(output_path)


def _generate_huggingface(prompt: str, output_path: Path) -> None:
    from huggingface_hub import InferenceClient

    settings = get_settings()
    if not settings["hf_token"]:
        raise RuntimeError(
            "HF_TOKEN is missing. Add it to .env or set IMAGE_BACKEND=placeholder."
        )

    client = InferenceClient(
        provider="auto",
        api_key=settings["hf_token"],
    )
    image = client.text_to_image(
        prompt=prompt,
        model=settings["hf_image_model"],
    )
    image.save(output_path)


def _generate_local_diffusers(prompt: str, output_path: Path) -> None:
    import torch
    from diffusers import DiffusionPipeline

    settings = get_settings()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = DiffusionPipeline.from_pretrained(
        settings["local_image_model"],
        torch_dtype=dtype,
    )
    pipe = pipe.to(device)

    result = pipe(
        prompt=prompt,
        width=settings["image_width"],
        height=settings["image_height"],
        num_inference_steps=20,
    )
    result.images[0].save(output_path)


def generate_image(image_prompt: str, panel_number: int) -> str:
    settings = get_settings()
    PANELS_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{panel_number:02d}-{_safe_name(image_prompt)}-{uuid.uuid4().hex[:8]}.png"
    output_path = PANELS_DIR / filename

    enhanced_prompt = (
        f"{image_prompt}. Consistent comic illustration, clean composition, "
        f"clear subject, expressive characters, no text, no watermark."
    )

    try:
        if settings["image_backend"] == "hf":
            _generate_huggingface(enhanced_prompt, output_path)
        elif settings["image_backend"] == "local":
            _generate_local_diffusers(enhanced_prompt, output_path)
        elif settings["image_backend"] == "placeholder":
            _placeholder_image(
                enhanced_prompt,
                output_path,
                settings["image_width"],
                settings["image_height"],
            )
        else:
            raise RuntimeError(
                "IMAGE_BACKEND must be hf, local, or placeholder."
            )
    except Exception as exc:
        # Do not crash the whole comic if an image provider temporarily fails.
        _placeholder_image(
            f"Panel {panel_number}: {enhanced_prompt}\nError: {exc}",
            output_path,
            settings["image_width"],
            settings["image_height"],
        )

    return f"/static/panels/{filename}"
