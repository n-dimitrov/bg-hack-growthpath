from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.assessment import Assessment
from ..schemas.assessment import AssessmentCreate, AssessmentResponse

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("/", response_model=AssessmentResponse)
def create_assessment(
    assessment: AssessmentCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new skill assessment for a user"""
    db_assessment = Assessment(
        user_id=user_id,
        competency_id=assessment.competency_id,
        proficiency_level=assessment.proficiency_level
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.get("/user/{user_id}", response_model=List[AssessmentResponse])
def get_user_assessments(user_id: int, db: Session = Depends(get_db)):
    """Get all assessments for a specific user"""
    assessments = db.query(Assessment).filter(Assessment.user_id == user_id).all()
    return assessments
