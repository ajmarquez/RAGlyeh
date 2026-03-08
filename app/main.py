from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.stories import router as stories_router

app = FastAPI()
app.include_router(health_router)
app.include_router(stories_router)


@app.get("/")
def root():
    return {"message": "RAGlyeh API is running"}
