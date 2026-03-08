from pydantic import BaseModel
from datetime import datetime

class StoryCreate(BaseModel):
    title: str
    author: str | None = None
    source_url: str | None = None
    text: str

class Story(BaseModel):
    id: str
    title: str
    author: str | None
    source_url: str | None
    text: str
    created_at: datetime
    
