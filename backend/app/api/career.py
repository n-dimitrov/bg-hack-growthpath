"""Career framework API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from pathlib import Path

from app.core.database import get_db
from app.models.career import (
    CareerLevel,
    CompetencyArea,
    CompetencyExpectation,
    Skill,
    DevelopmentPlan,
    LearningObjective
)

router = APIRouter(prefix="/api/career", tags=["career"])


# Helper function to load JSON files
def load_framework_json():
    """Load CareerFramework.json"""
    file_path = Path(__file__).parent.parent.parent.parent / 'CareerFramework.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@router.get("/paths")
def get_career_paths():
    """
    Get all available career tracks

    Returns:
        List of career tracks with their details
    """
    framework = load_framework_json()

    tracks = []
    for key, data in framework['career_tracks'].items():
        tracks.append({
            "key": key,
            "name": data['name'],
            "description": data['description'],
            "levels": len(data['levels']),
            "level_details": [
                {
                    "level": level['level'],
                    "title": level['title'],
                    "pay_class": level['pay_class'],
                    "summary": level['summary']
                }
                for level in data['levels']
            ]
        })

    return {"tracks": tracks}


@router.get("/paths/{track}/{pay_class}")
def get_level_details(track: str, pay_class: str, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific career level

    Args:
        track: Career track (e.g., 'software_engineer')
        pay_class: Pay class (e.g., 'PC08')

    Returns:
        Level details with competencies
    """
    framework = load_framework_json()

    track_data = framework['career_tracks'].get(track)
    if not track_data:
        raise HTTPException(status_code=404, detail="Career track not found")

    level = next((l for l in track_data['levels'] if l['pay_class'] == pay_class), None)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    # Get competencies from database
    competencies = []
    competency_areas = db.query(CompetencyArea).all()

    for area in competency_areas:
        expectation = db.query(CompetencyExpectation).filter(
            CompetencyExpectation.competency_area_id == area.id,
            CompetencyExpectation.pay_class == pay_class
        ).first()

        if expectation:
            competencies.append({
                "area_key": area.area_key,
                "area": area.name,
                "description": area.description,
                "expectations": expectation.expectations,
                "scope": expectation.scope
            })

    return {
        **level,
        "competencies": competencies,
        "total_competencies": len(competencies)
    }


@router.get("/competencies")
def get_all_competencies(pay_class: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all competency areas, optionally filtered by pay class

    Args:
        pay_class: Optional pay class filter (e.g., 'PC08')

    Returns:
        List of competency areas with expectations
    """
    competencies = []
    areas = db.query(CompetencyArea).all()

    for area in areas:
        comp_data = {
            "id": area.id,
            "area_key": area.area_key,
            "name": area.name,
            "description": area.description,
            "expectations": []
        }

        # Get expectations
        query = db.query(CompetencyExpectation).filter(
            CompetencyExpectation.competency_area_id == area.id
        )

        if pay_class:
            query = query.filter(CompetencyExpectation.pay_class == pay_class)

        expectations = query.all()

        for exp in expectations:
            comp_data["expectations"].append({
                "pay_class": exp.pay_class,
                "expectations": exp.expectations,
                "scope": exp.scope
            })

        if comp_data["expectations"]:  # Only include if has expectations
            competencies.append(comp_data)

    return {
        "competencies": competencies,
        "total": len(competencies)
    }


@router.post("/skills-gap")
def calculate_skills_gap(current_level: str, target_level: str, db: Session = Depends(get_db)):
    """
    Calculate skills gap between current and target levels

    Args:
        current_level: Current pay class (e.g., 'PC07')
        target_level: Target pay class (e.g., 'PC08')

    Returns:
        List of competency gaps
    """
    gaps = []
    areas = db.query(CompetencyArea).all()

    for area in areas:
        # Get current level expectations
        current_exp = db.query(CompetencyExpectation).filter(
            CompetencyExpectation.competency_area_id == area.id,
            CompetencyExpectation.pay_class == current_level
        ).first()

        # Get target level expectations
        target_exp = db.query(CompetencyExpectation).filter(
            CompetencyExpectation.competency_area_id == area.id,
            CompetencyExpectation.pay_class == target_level
        ).first()

        # Only include if both exist and are different
        if current_exp and target_exp and current_exp.expectations != target_exp.expectations:
            gaps.append({
                "competency_area_id": area.id,
                "area": area.name,
                "description": area.description,
                "current": current_exp.expectations,
                "required": target_exp.expectations,
                "gap_summary": f"Need to progress from '{current_level}' to '{target_level}' level"
            })

    return {
        "current_level": current_level,
        "target_level": target_level,
        "gaps": gaps,
        "total_gaps": len(gaps)
    }


@router.post("/development-plan")
def generate_development_plan(
    user_id: int,
    current_level: str,
    target_level: str,
    db: Session = Depends(get_db)
):
    """
    Generate a personalized development plan

    Args:
        user_id: User ID
        current_level: Current pay class
        target_level: Target pay class

    Returns:
        Development plan with learning objectives
    """
    from datetime import date, timedelta

    # Calculate skills gap
    gap_data = calculate_skills_gap(current_level, target_level, db)

    # Create development plan
    plan = DevelopmentPlan(
        user_id=user_id,
        current_level=current_level,
        target_level=target_level,
        created_date=date.today(),
        target_date=date.today() + timedelta(days=180),  # 6 months
        status='active'
    )
    db.add(plan)
    db.flush()

    # Create learning objectives
    objectives = []
    for idx, gap in enumerate(gap_data['gaps']):
        priority = 'High' if idx < 3 else 'Medium' if idx < 6 else 'Low'

        objective = LearningObjective(
            plan_id=plan.id,
            competency_area_id=gap['competency_area_id'],
            description=f"Achieve {target_level} level competency in {gap['area']}",
            priority=priority,
            status='not_started'
        )
        db.add(objective)

        objectives.append({
            "id": idx + 1,
            "competency": gap['area'],
            "current_state": gap['current'],
            "target_state": gap['required'],
            "priority": priority,
            "status": 'not_started'
        })

    db.commit()

    return {
        "plan_id": plan.id,
        "user_id": user_id,
        "current_level": current_level,
        "target_level": target_level,
        "created_date": str(plan.created_date),
        "target_date": str(plan.target_date),
        "objectives": objectives,
        "total_objectives": len(objectives),
        "estimated_timeframe": "6 months"
    }


@router.get("/development-plan/{plan_id}")
def get_development_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get a specific development plan"""
    plan = db.query(DevelopmentPlan).filter(DevelopmentPlan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Development plan not found")

    # Get objectives
    objectives = []
    for obj in plan.objectives:
        objectives.append({
            "id": obj.id,
            "competency": obj.competency_area.name if obj.competency_area else "General",
            "description": obj.description,
            "priority": obj.priority,
            "status": obj.status
        })

    return {
        "plan_id": plan.id,
        "user_id": plan.user_id,
        "current_level": plan.current_level,
        "target_level": plan.target_level,
        "created_date": str(plan.created_date),
        "target_date": str(plan.target_date),
        "status": plan.status,
        "objectives": objectives
    }


@router.get("/levels")
def get_all_career_levels(track: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all career levels from database

    Args:
        track: Optional filter by career track

    Returns:
        List of career levels
    """
    query = db.query(CareerLevel)

    if track:
        query = query.filter(CareerLevel.track == track)

    levels = query.order_by(CareerLevel.level).all()

    return {
        "levels": [
            {
                "id": level.id,
                "track": level.track,
                "level": level.level,
                "title": level.title,
                "pay_class": level.pay_class,
                "summary": level.summary,
                "impact_scope": level.impact_scope
            }
            for level in levels
        ],
        "total": len(levels)
    }


@router.get("/user-plans/{user_id}")
def get_user_plans(user_id: int, db: Session = Depends(get_db)):
    """
    Get all development plans for a user

    Args:
        user_id: User ID

    Returns:
        List of development plans with progress
    """
    plans = db.query(DevelopmentPlan).filter(
        DevelopmentPlan.user_id == user_id
    ).order_by(DevelopmentPlan.created_date.desc()).all()

    result = []
    for plan in plans:
        objectives = plan.objectives
        total = len(objectives)
        completed = sum(1 for obj in objectives if obj.status == 'completed')
        in_progress = sum(1 for obj in objectives if obj.status == 'in_progress')
        not_started = sum(1 for obj in objectives if obj.status == 'not_started')

        result.append({
            "plan_id": plan.id,
            "current_level": plan.current_level,
            "target_level": plan.target_level,
            "created_date": str(plan.created_date),
            "target_date": str(plan.target_date) if plan.target_date else None,
            "status": plan.status,
            "total_objectives": total,
            "completed_objectives": completed,
            "in_progress_objectives": in_progress,
            "not_started_objectives": not_started,
            "completion_percentage": round((completed / total * 100) if total > 0 else 0, 1)
        })

    return {"plans": result, "total": len(result)}


@router.put("/objective/{objective_id}")
def update_objective_status(objective_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update learning objective status

    Args:
        objective_id: Objective ID
        status: New status (not_started, in_progress, completed)

    Returns:
        Updated objective
    """
    valid_statuses = ['not_started', 'in_progress', 'completed']
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    objective = db.query(LearningObjective).filter(LearningObjective.id == objective_id).first()

    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    objective.status = status
    db.commit()
    db.refresh(objective)

    return {
        "id": objective.id,
        "description": objective.description,
        "status": objective.status,
        "priority": objective.priority,
        "message": f"Objective status updated to '{status}'"
    }


@router.put("/plan/{plan_id}/status")
def update_plan_status(plan_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update development plan status

    Args:
        plan_id: Plan ID
        status: New status (active, completed, cancelled)

    Returns:
        Updated plan
    """
    valid_statuses = ['active', 'completed', 'cancelled']
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    plan = db.query(DevelopmentPlan).filter(DevelopmentPlan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.status = status
    db.commit()
    db.refresh(plan)

    return {
        "plan_id": plan.id,
        "status": plan.status,
        "message": f"Plan status updated to '{status}'"
    }
