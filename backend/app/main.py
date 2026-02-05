from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api import competencies, assessments

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
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(competencies.router)
app.include_router(assessments.router)


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
