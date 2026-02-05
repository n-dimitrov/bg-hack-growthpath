from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.competency import Competency
from ..schemas.competency import CompetencyCreate, CompetencyResponse

router = APIRouter(prefix="/competencies", tags=["competencies"])


@router.post("/", response_model=CompetencyResponse)
def create_competency(
    competency: CompetencyCreate,
    db: Session = Depends(get_db)
):
    """Create a new competency"""
    db_competency = Competency(**competency.dict())
    db.add(db_competency)
    db.commit()
    db.refresh(db_competency)
    return db_competency


@router.get("/", response_model=List[CompetencyResponse])
def list_competencies(db: Session = Depends(get_db)):
    """Get all available competencies"""
    competencies = db.query(Competency).all()
    return competencies


@router.get("/{competency_id}", response_model=CompetencyResponse)
def get_competency(competency_id: int, db: Session = Depends(get_db)):
    """Get a specific competency by ID"""
    competency = db.query(Competency).filter(Competency.id == competency_id).first()
    if not competency:
        raise HTTPException(status_code=404, detail="Competency not found")
    return competency
