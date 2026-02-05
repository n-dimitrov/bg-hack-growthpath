from pydantic import BaseModel
from typing import Optional
from ..models.competency import CompetencyCategory


class CompetencyBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: CompetencyCategory


class CompetencyCreate(CompetencyBase):
    pass


class CompetencyResponse(CompetencyBase):
    id: int

    class Config:
        from_attributes = True
