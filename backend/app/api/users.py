from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
import httpx
from ..core.database import get_db
from ..models.user import User
from ..models.competency import Competency, CompetencyCategory
from ..models.assessment import Assessment, ProficiencyLevel

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get list of all users with optional search

    Query Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - search: Search by name or email
    """
    query = db.query(User)

    # Apply search filter if provided
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.name.ilike(search_filter)) |
            (User.email.ilike(search_filter))
        )

    # Get total count
    total = query.count()

    # Apply pagination
    users = query.offset(skip).limit(limit).all()

    # Enrich user data with skill counts
    user_list = []
    for user in users:
        skills_count = db.query(Assessment).filter(
            Assessment.user_id == user.id
        ).count()

        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "skills_count": skills_count
        })

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": user_list
    }


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed information about a specific user"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get skills count
    skills_count = db.query(Assessment).filter(
        Assessment.user_id == user_id
    ).count()

    # Get skills by category
    skills_by_category = {}
    for category in CompetencyCategory:
        count = db.query(Assessment).join(Competency).filter(
            Assessment.user_id == user_id,
            Competency.category == category
        ).count()
        if count > 0:
            skills_by_category[category.value] = count

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "skills_count": skills_count,
        "skills_by_category": skills_by_category
    }


@router.get("/{user_id}/skills")
def get_user_skills(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get all skills/competencies for a specific user grouped by category"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all assessments for the user
    assessments = db.query(Assessment).filter(
        Assessment.user_id == user_id
    ).all()

    # Group by category
    skills_by_category = {}
    total_skills = 0

    for assessment in assessments:
        competency = db.query(Competency).filter(
            Competency.id == assessment.competency_id
        ).first()

        if competency:
            category = competency.category.value

            if category not in skills_by_category:
                skills_by_category[category] = {
                    "category": category,
                    "competencies": []
                }

            skills_by_category[category]["competencies"].append({
                "id": competency.id,
                "name": competency.name,
                "description": competency.description,
                "proficiency_level": assessment.proficiency_level.value,
                "proficiency_name": assessment.proficiency_level.name,
                "assessed_at": assessment.assessed_at.isoformat() if assessment.assessed_at else None
            })
            total_skills += 1

    # Convert to list and sort by category
    skills_list = list(skills_by_category.values())

    # Count by category
    category_counts = {
        cat["category"]: len(cat["competencies"])
        for cat in skills_list
    }

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value
        },
        "skills": skills_list,
        "total_skills": total_skills,
        "by_category": category_counts
    }


@router.get("/search/by-skill/{competency_id}")
def get_users_by_skill(
    competency_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all users who have a specific skill/competency"""
    competency = db.query(Competency).filter(
        Competency.id == competency_id
    ).first()

    if not competency:
        raise HTTPException(status_code=404, detail="Competency not found")

    # Get all users with this competency
    assessments = db.query(Assessment).filter(
        Assessment.competency_id == competency_id
    ).all()

    users_with_skill = []
    proficiency_distribution = {
        "BEGINNER": 0,
        "INTERMEDIATE": 0,
        "ADVANCED": 0,
        "EXPERT": 0
    }

    for assessment in assessments:
        user = db.query(User).filter(User.id == assessment.user_id).first()
        if user:
            users_with_skill.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "proficiency_level": assessment.proficiency_level.value,
                "proficiency_name": assessment.proficiency_level.name,
                "assessed_at": assessment.assessed_at.isoformat() if assessment.assessed_at else None
            })
            proficiency_distribution[assessment.proficiency_level.name] += 1

    return {
        "competency": {
            "id": competency.id,
            "name": competency.name,
            "description": competency.description,
            "category": competency.category.value
        },
        "total_users": len(users_with_skill),
        "users": users_with_skill,
        "proficiency_distribution": proficiency_distribution
    }


@router.post("/{user_id}/analyze-skills")
async def analyze_user_skills(
    user_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze user's skills with LLM to identify gaps, recommendations, and career paths
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user's skills
    assessments = db.query(Assessment).filter(
        Assessment.user_id == user_id
    ).all()

    if not assessments:
        raise HTTPException(
            status_code=400,
            detail="User has no skills to analyze"
        )

    # Build skills data
    skills_data = []
    skills_by_category = {}

    for assessment in assessments:
        competency = db.query(Competency).filter(
            Competency.id == assessment.competency_id
        ).first()

        if competency:
            skill_info = {
                "name": competency.name,
                "category": competency.category.value,
                "proficiency": assessment.proficiency_level.name,
                "description": competency.description or ""
            }
            skills_data.append(skill_info)

            # Group by category
            category = competency.category.value
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill_info)

    # Build LLM prompt
    skills_summary = "\n".join([
        f"- {skill['name']} ({skill['category']}): {skill['proficiency']}"
        for skill in skills_data
    ])

    system_prompt = """You are an expert career advisor and skills analyst.
Analyze the employee's current skills and provide actionable insights.
Focus on identifying skill gaps, missing competencies, and career development opportunities.
Provide specific, practical recommendations."""

    user_prompt = f"""Analyze the following employee profile:

**Employee:** {user.name}
**Role:** {user.role.value}
**Current Skills ({len(skills_data)} total):**

{skills_summary}

**Skills by Category:**
{chr(10).join([f"- {cat}: {len(skills)} skills" for cat, skills in skills_by_category.items()])}

Please provide:

1. **Skill Gaps Analysis:**
   - What important skills are missing for their role?
   - Which skill categories need strengthening?
   - Are there proficiency level gaps (e.g., too many beginner skills)?

2. **Recommendations:**
   - Top 5 skills to develop next
   - Suggest learning paths or resources
   - Prioritize by impact on career growth

3. **Career Opportunities:**
   - What roles could they pursue with current skills?
   - What additional skills needed for advancement?
   - Suggested career progression path

4. **Strengths:**
   - What are their strongest skill areas?
   - Unique skill combinations they have

Format your response in clear sections with bullet points. Be specific and actionable."""

    try:
        # Call LLM API endpoint
        async with httpx.AsyncClient() as client:
            llm_response = await client.post(
                "http://localhost:8000/api/llm/chat",
                json={
                    "user_content": user_prompt,
                    "system_content": system_prompt,
                    "max_tokens": 2000
                },
                timeout=60.0
            )
            llm_response.raise_for_status()
            llm_data = llm_response.json()

        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value
            },
            "skills_analyzed": len(skills_data),
            "skills_by_category": {
                cat: len(skills) for cat, skills in skills_by_category.items()
            },
            "analysis": llm_data.get("content", [{}])[0].get("text", ""),
            "model_used": llm_data.get("model", "unknown")
        }

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            error_detail = e.response.json().get("detail", "LLM service error")
            if "not configured" in error_detail.lower():
                raise HTTPException(
                    status_code=503,
                    detail="LLM service not configured. Please set LLM_FARM_API_KEY."
                )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"LLM API error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
