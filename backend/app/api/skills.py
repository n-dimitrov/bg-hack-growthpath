"""Skills catalog API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from pathlib import Path

from app.core.database import get_db
from app.models.career import Skill, UserSkill

router = APIRouter(prefix="/api/skills", tags=["skills"])


def load_tech_skills_json():
    """Load TechMasterData.json"""
    file_path = Path(__file__).parent.parent.parent.parent / 'TechMasterData.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@router.get("/catalog")
def get_skills_catalog(
    category: Optional[str] = None,
    search: Optional[str] = None,
    skill_type: Optional[str] = Query(None, description="Filter by: data, tech, or all"),
    db: Session = Depends(get_db)
):
    """
    Get skills catalog with optional filtering

    Args:
        category: Filter by parent category
        search: Search in skill name or description
        skill_type: Filter by skill type (data, tech, or all)

    Returns:
        List of skills
    """
    query = db.query(Skill)

    # Filter by skill type
    if skill_type == 'data':
        query = query.filter(Skill.is_data_skill == 1)
    elif skill_type == 'tech':
        query = query.filter(Skill.is_data_skill == 0)

    # Filter by category
    if category:
        query = query.filter(Skill.parent_category == category)

    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Skill.name.ilike(search_term)) |
            (Skill.description.ilike(search_term))
        )

    skills = query.all()

    return {
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "category": skill.parent_category,
                "description": skill.description,
                "skill_category": skill.category,
                "roles": skill.roles,
                "is_data_skill": bool(skill.is_data_skill)
            }
            for skill in skills
        ],
        "total": len(skills)
    }


@router.get("/categories")
def get_skill_categories(db: Session = Depends(get_db)):
    """
    Get all unique skill categories

    Returns:
        List of categories with skill counts
    """
    # Get unique parent categories
    from sqlalchemy import func

    categories = db.query(
        Skill.parent_category,
        func.count(Skill.id).label('count')
    ).group_by(Skill.parent_category).all()

    # Also get skill categories (Standard, Advanced, etc.)
    skill_categories = db.query(
        Skill.category,
        func.count(Skill.id).label('count')
    ).filter(Skill.category.isnot(None)).group_by(Skill.category).all()

    return {
        "parent_categories": [
            {
                "name": cat[0] if cat[0] else "Uncategorized",
                "count": cat[1]
            }
            for cat in categories
        ],
        "skill_categories": [
            {
                "name": cat[0],
                "count": cat[1]
            }
            for cat in skill_categories
        ]
    }


@router.get("/hierarchical")
def get_hierarchical_skills():
    """
    Get skills in hierarchical structure from TechMasterData.json

    Returns:
        Hierarchical skill structure
    """
    tech_data = load_tech_skills_json()

    return {
        "hierarchical": tech_data['hierarchical'],
        "metadata": tech_data['metadata']
    }


@router.get("/recommend/{pay_class}")
def recommend_skills(pay_class: str, db: Session = Depends(get_db)):
    """
    Recommend skills for a specific career level

    Args:
        pay_class: Career level (e.g., 'PC08')

    Returns:
        Recommended skills based on level
    """
    # Map pay class to skill categories
    proficiency_map = {
        'PC06': ['Standard'],  # Junior - focus on standard skills
        'PC07': ['Standard'],  # Mid - standard skills
        'PC08': ['Standard', 'Advanced'],  # Senior - add advanced
        'PC09': ['Standard', 'Advanced', 'Niche'],  # Lead - add niche
        'PC10': ['Standard', 'Advanced', 'Niche']  # Principal - all
    }

    recommended_categories = proficiency_map.get(pay_class, ['Standard'])

    # Get skills from database
    skills = db.query(Skill).filter(
        Skill.category.in_(recommended_categories),
        Skill.category != 'Inactive'
    ).all()

    # Group by category
    categorized_skills = {}
    for skill in skills:
        cat = skill.category or 'Other'
        if cat not in categorized_skills:
            categorized_skills[cat] = []

        categorized_skills[cat].append({
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "roles": skill.roles
        })

    return {
        "pay_class": pay_class,
        "recommended_categories": recommended_categories,
        "skills_by_category": categorized_skills,
        "total_skills": len(skills)
    }


@router.post("/user-skill")
def add_user_skill(
    user_id: int,
    skill_id: int,
    proficiency_level: str,
    db: Session = Depends(get_db)
):
    """
    Add or update user skill assessment

    Args:
        user_id: User ID
        skill_id: Skill ID
        proficiency_level: beginner, intermediate, advanced, or expert

    Returns:
        Created/updated user skill
    """
    from datetime import date

    # Validate proficiency level
    valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    if proficiency_level not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid proficiency level. Must be one of: {', '.join(valid_levels)}"
        )

    # Check if skill exists
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check if user already has this skill
    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_id == skill_id
    ).first()

    if user_skill:
        # Update existing
        user_skill.proficiency_level = proficiency_level
        user_skill.last_assessed = date.today()
    else:
        # Create new
        user_skill = UserSkill(
            user_id=user_id,
            skill_id=skill_id,
            proficiency_level=proficiency_level,
            last_assessed=date.today()
        )
        db.add(user_skill)

    db.commit()
    db.refresh(user_skill)

    return {
        "id": user_skill.id,
        "user_id": user_skill.user_id,
        "skill": {
            "id": skill.id,
            "name": skill.name,
            "category": skill.parent_category
        },
        "proficiency_level": user_skill.proficiency_level,
        "last_assessed": str(user_skill.last_assessed)
    }


@router.get("/user-skills/{user_id}")
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    """
    Get all skills for a specific user

    Args:
        user_id: User ID

    Returns:
        List of user skills with proficiency levels
    """
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()

    skills_data = []
    for us in user_skills:
        skills_data.append({
            "id": us.id,
            "skill": {
                "id": us.skill.id,
                "name": us.skill.name,
                "category": us.skill.parent_category,
                "description": us.skill.description
            },
            "proficiency_level": us.proficiency_level,
            "last_assessed": str(us.last_assessed) if us.last_assessed else None
        })

    # Group by proficiency level
    by_proficiency = {}
    for skill in skills_data:
        level = skill['proficiency_level']
        if level not in by_proficiency:
            by_proficiency[level] = []
        by_proficiency[level].append(skill)

    return {
        "user_id": user_id,
        "skills": skills_data,
        "total_skills": len(skills_data),
        "by_proficiency": by_proficiency
    }


@router.get("/{skill_id}")
def get_skill_details(skill_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific skill

    Args:
        skill_id: Skill ID

    Returns:
        Skill details
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return {
        "id": skill.id,
        "name": skill.name,
        "category": skill.parent_category,
        "description": skill.description,
        "skill_category": skill.category,
        "roles": skill.roles,
        "is_data_skill": bool(skill.is_data_skill)
    }
