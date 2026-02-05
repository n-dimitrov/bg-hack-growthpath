"""Career framework database models"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class CareerLevel(Base):
    """Career levels (e.g., Junior Engineer, Senior Engineer)"""
    __tablename__ = "career_levels"

    id = Column(Integer, primary_key=True, index=True)
    track = Column(String(50), nullable=False)  # 'software_engineer' or 'software_architect'
    level = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    pay_class = Column(String(10), nullable=False, index=True)
    summary = Column(Text)
    impact_scope = Column(Text)
    project_category = Column(String(10), nullable=True)  # For architects


class CompetencyArea(Base):
    """Competency areas (e.g., Design, Quality, Operations)"""
    __tablename__ = "competency_areas"

    id = Column(Integer, primary_key=True, index=True)
    area_key = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    expectations = relationship("CompetencyExpectation", back_populates="competency_area")


class CompetencyExpectation(Base):
    """Expected competency levels for each pay class"""
    __tablename__ = "competency_expectations"

    id = Column(Integer, primary_key=True, index=True)
    competency_area_id = Column(Integer, ForeignKey("competency_areas.id"))
    pay_class = Column(String(10), nullable=False, index=True)
    expectations = Column(Text, nullable=False)
    scope = Column(String(100), nullable=True)

    competency_area = relationship("CompetencyArea", back_populates="expectations")


class Skill(Base):
    """Skills catalog (technologies, tools, methodologies)"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    parent_category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # Standard, Advanced, Niche, Inactive
    roles = Column(Text, nullable=True)  # JSON string of applicable roles
    is_data_skill = Column(Integer, default=0)  # 1 if from Skillsets.json


class UserSkill(Base):
    """User skill assessments"""
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"))
    proficiency_level = Column(String(20), nullable=False)  # beginner, intermediate, advanced, expert
    last_assessed = Column(Date, nullable=True)

    skill = relationship("Skill")


class DevelopmentPlan(Base):
    """User development plans"""
    __tablename__ = "development_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    current_level = Column(String(10), nullable=False)
    target_level = Column(String(10), nullable=False)
    created_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=True)
    status = Column(String(20), default='active')  # active, completed, cancelled

    objectives = relationship("LearningObjective", back_populates="plan")


class LearningObjective(Base):
    """Learning objectives within development plans"""
    __tablename__ = "learning_objectives"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("development_plans.id"))
    competency_area_id = Column(Integer, ForeignKey("competency_areas.id"), nullable=True)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default='Medium')  # High, Medium, Low
    status = Column(String(20), default='not_started')  # not_started, in_progress, completed

    plan = relationship("DevelopmentPlan", back_populates="objectives")
    competency_area = relationship("CompetencyArea")
