from typing import List

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(default="Alex", min_length=1, max_length=80)
    setting: str = Field(default="enchanted forest", min_length=1, max_length=120)
    tone: str = Field(default="dramatic", min_length=1, max_length=60)
    art_style: str = Field(default="comic book", min_length=1, max_length=80)


class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str


class OutlineResponse(BaseModel):
    panels: List[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    caption: str
    narration: str


class StoryResponse(BaseModel):
    panels: List[PanelStory]
