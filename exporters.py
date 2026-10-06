from pathlib import Path
from datetime import datetime
from fpdf import FPDF


def _clean_text(text) -> str:
    """Make text safe for the PDF's built-in Helvetica font."""
    if text is None:
        return ""

    text = str(text)

    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "-",
        "✨": "*",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode("latin-1", "replace").decode("latin-1")


def save_pdf(layout: list[dict]) -> str:
    output_dir = Path("generated")
    output_dir.mkdir(exist_ok=True)

    filename = f"comiccraft-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
    output = output_dir / filename

    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    page_width = 210
    left_margin = 15
    right_margin = 15
    usable_width = page_width - left_margin - right_margin

    for panel in layout:
        pdf.add_page()

        # Panel title
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_x(left_margin)
        pdf.multi_cell(
            usable_width,
            10,
            _clean_text(
                f"Panel {panel.get('panel_number', '')}: "
                f"{panel.get('title', '')}"
            ),
        )

        # Image
        image_path = panel.get("image_path")

        if image_path and Path(image_path).exists():
            try:
                draw_w = 170
                draw_h = 120

                pdf.image(
                    str(image_path),
                    x=(page_width - draw_w) / 2,
                    w=draw_w,
                    h=draw_h,
                )

                pdf.ln(5)

            except Exception:
                pdf.ln(5)

        # Scene description
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_x(left_margin)
        pdf.multi_cell(
            usable_width,
            6,
            _clean_text(panel.get("scene_description", "")),
        )

        pdf.ln(2)

        # Caption
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_x(left_margin)
        pdf.multi_cell(
            usable_width,
            6,
            _clean_text(
                f"Caption: {panel.get('caption', '')}"
            ),
        )

        pdf.ln(1)

        # Narration
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(left_margin)
        pdf.multi_cell(
            usable_width,
            6,
            _clean_text(panel.get("narration", "")),
        )

        # Dialogue
        dialogue = panel.get("dialogue", "")

        if dialogue:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(left_margin)
            pdf.multi_cell(
                usable_width,
                6,
                _clean_text(f"Dialogue: {dialogue}"),
            )

    pdf.output(str(output))

    return str(output)