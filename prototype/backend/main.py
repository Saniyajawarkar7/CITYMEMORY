from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes.assets import router as assets_router
from routes.events import router as events_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CITYMEMORY API",
    description="Institutional Memory & Recurring-Failure Intelligence System",
    version="1.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets_router)
app.include_router(events_router)

@app.get("/")
def root():
    return {
        "system": "CITYMEMORY",
        "status": "running",
        "message": "Institutional Memory Engine"
    }
