from pydantic import BaseModel
from datetime import datetime 

class StoryRequest(BaseModel):
    title: str
    content: str
    
class StoryResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    
