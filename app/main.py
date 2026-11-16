from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()
settings.prepare()
app = FastAPI(title="Atlas — Autonomous AI Research Agent", version="1.0.0",
    description="Tool-using AI agent built with LangGraph, Groq, FastAPI and SQLite.")
app.include_router(router, prefix="/api", tags=["agent"])

@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(Path(__file__).resolve().parent.parent / "ui" / "index.html")

@app.get("/health", tags=["system"])
def health():
    return {"status":"ok", "service":"atlas-agent"}
