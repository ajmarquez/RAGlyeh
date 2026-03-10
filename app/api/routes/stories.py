from fastapi import APIRouter, HTTPException

from uuid import uuid4
from datetime import datetime, timezone

from app.models.story import StoryCreate, Story  

router = APIRouter()

STORY_STORE: dict[str, Story] = {}

@router.post("/stories", response_model=Story, status_code=201)
def create_story(story: StoryCreate):
    
    if not story.text.strip():
        raise HTTPException(status_code=400, detail="Story text cannot be empty")
    
    created_story = Story(
        id=str(uuid4()),
        title=story.title,
        author=story.author,
        source_url=story.source_url,
        text=story.text,
        created_at=datetime.now(timezone.utc)
    )
    
    STORY_STORE[created_story.id] = created_story
    return created_story

@router.get("/stories/{story_id}")
def get_story(story_id: str):
    if story_id not in STORY_STORE:
        raise HTTPException(status_code=404, detail="Story not found")
    return STORY_STORE[story_id]

@router.get("/stories")
def list_stories():
    # Return all stories from the in-memory store
    if not STORY_STORE:
        return []
    return list(STORY_STORE.values())  