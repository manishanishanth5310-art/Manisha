def build_comic_layout(story_panels: list[dict], image_paths: list[str]) -> list[dict]:
    if len(story_panels) != len(image_paths):
        raise ValueError("Each story panel must have exactly one image.")

    layout = []
    for panel, image_path in zip(story_panels, image_paths):
        item = dict(panel)
        item["image_path"] = image_path
        layout.append(item)
    return layout
