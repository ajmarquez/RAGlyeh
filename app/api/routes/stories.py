from fastapi import APIRouter, HTTPException

from uuid import uuid4
from datetime import datetime, timezone

from app.models.story import StoryCreate, Story  

router = APIRouter()

STORY_STORE: dict[str, Story] = {}

@router.post("/stories", response_model=Story, status_code= 201)
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
    # For demonstration, we return a dummy story. In a real application, you'd fetch this from a database.
    story = Story(
        id=story_id,
        title="Sample Story",
        author=None,
        source_url=None,
        text="This is a sample story content.",
        created_at=datetime.now(timezone.utc)
    )
    return story

@router.get("/stories")
def list_stories():
    # For demonstration, we return a list of dummy stories. In a real application, you'd fetch this from a database.
    stories = [
        Story(
            id=str(uuid4()),
            title="Sample Story 1",
            author=None,
            source_url=None,
            text="This is the first sample story content.",
            created_at=datetime.now(timezone.utc)
        ),
        Story(
            id=str(uuid4()),
            title="Sample Story 2",
            author=None,
            source_url=None,
            text="This is the second sample story content.",
            created_at=datetime.now(timezone.utc)
        )
    ]
    return stories  