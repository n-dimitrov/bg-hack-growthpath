from pydantic import BaseModel
from datetime import datetime
from ..models.assessment import ProficiencyLevel


class AssessmentBase(BaseModel):
    competency_id: int
    proficiency_level: ProficiencyLevel


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentResponse(AssessmentBase):
    id: int
    user_id: int
    assessed_at: datetime

    class Config:
        from_attributes = True
