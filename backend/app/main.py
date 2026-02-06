from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.database import engine, Base
from .api import competencies, assessments, career, skills, llm
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GrowthPath API",
    description="Competence Management System API",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(competencies.router)
app.include_router(assessments.router)
app.include_router(career.router)
app.include_router(skills.router)
app.include_router(llm.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to GrowthPath API",
        "docs": "/docs",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/tester")
def llm_tester_page():
    """Serve the LLM tester page"""
    # Go up from app/ to backend/, then to static/
    backend_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(backend_dir, "static", "llm-tester.html")
    return FileResponse(file_path, media_type="text/html")
