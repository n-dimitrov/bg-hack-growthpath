from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class CompetencyCategory(enum.Enum):
    TECHNICAL = "technical"
    SOFT_SKILLS = "soft_skills"
    LEADERSHIP = "leadership"
    DOMAIN_KNOWLEDGE = "domain_knowledge"


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(Enum(CompetencyCategory), nullable=False)

    # Relationships
    assessments = relationship("Assessment", back_populates="competency", cascade="all, delete-orphan")
