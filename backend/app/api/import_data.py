from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
import pandas as pd
import tempfile
import os
from passlib.context import CryptContext
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.competency import Competency, CompetencyCategory
from ..models.assessment import Assessment, ProficiencyLevel

router = APIRouter(prefix="/import", tags=["import"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def map_skillset_level_to_proficiency(level: str) -> ProficiencyLevel:
    """Map Planisware skillset level to proficiency level"""
    level_mapping = {
        "1st": ProficiencyLevel.BEGINNER,
        "2nd": ProficiencyLevel.INTERMEDIATE,
        "3rd": ProficiencyLevel.ADVANCED,
        "4th": ProficiencyLevel.EXPERT
    }
    return level_mapping.get(level, ProficiencyLevel.BEGINNER)


def map_category_to_competency_category(category: str) -> CompetencyCategory:
    """Map Planisware category to competency category"""
    if pd.isna(category):
        return CompetencyCategory.TECHNICAL

    category = category.lower()

    if "standard" in category or "advanced" in category:
        return CompetencyCategory.TECHNICAL
    elif "leadership" in category:
        return CompetencyCategory.LEADERSHIP
    elif "niche" in category or "domain" in category:
        return CompetencyCategory.DOMAIN_KNOWLEDGE
    else:
        return CompetencyCategory.TECHNICAL


@router.post("/planisware")
async def import_planisware_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Import employee skillset data from Planisware Excel file

    Expected columns:
    - Name (required)
    - Skillset (required)
    - Skillset Level (required)
    - Skillsets.Description
    - Skillsets.Category
    - Skillsets.Role
    - Resource Location
    - Resource Country
    - Resource Region
    """

    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an Excel file (.xlsx or .xls)"
        )

    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Read Excel file
        df = pd.read_excel(tmp_file_path)

        # Validate required columns
        required_columns = ['Name', 'Skillset', 'Skillset Level']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )

        # Track statistics
        stats = {
            "users_created": 0,
            "users_existing": 0,
            "competencies_created": 0,
            "competencies_existing": 0,
            "assessments_created": 0,
            "assessments_existing": 0,
            "rows_processed": 0,
            "rows_skipped": 0,
            "errors": []
        }

        # Process each row
        for idx, row in df.iterrows():
            try:
                # Extract data
                name = row['Name']
                skillset = row['Skillset']
                skillset_level = row['Skillset Level']
                description = row.get('Skillsets.Description', '')
                category = row.get('Skillsets.Category', '')

                # Skip if essential data is missing
                if pd.isna(name) or pd.isna(skillset):
                    stats["rows_skipped"] += 1
                    continue

                # Create/Get User
                email = name.lower().replace(' ', '.') + '@bosch.com'
                user = db.query(User).filter(User.email == email).first()

                if not user:
                    user = User(
                        email=email,
                        name=name,
                        role=UserRole.EMPLOYEE,
                        hashed_password=pwd_context.hash('password123')
                    )
                    db.add(user)
                    db.flush()
                    stats["users_created"] += 1
                else:
                    stats["users_existing"] += 1

                # Create/Get Competency
                competency = db.query(Competency).filter(
                    Competency.name == skillset
                ).first()

                if not competency:
                    comp_category = map_category_to_competency_category(category)
                    competency = Competency(
                        name=skillset,
                        description=description if not pd.isna(description) else None,
                        category=comp_category
                    )
                    db.add(competency)
                    db.flush()
                    stats["competencies_created"] += 1
                else:
                    stats["competencies_existing"] += 1

                # Create Assessment
                proficiency = map_skillset_level_to_proficiency(skillset_level)

                existing_assessment = db.query(Assessment).filter(
                    Assessment.user_id == user.id,
                    Assessment.competency_id == competency.id,
                    Assessment.proficiency_level == proficiency
                ).first()

                if not existing_assessment:
                    assessment = Assessment(
                        user_id=user.id,
                        competency_id=competency.id,
                        proficiency_level=proficiency
                    )
                    db.add(assessment)
                    stats["assessments_created"] += 1
                else:
                    stats["assessments_existing"] += 1

                stats["rows_processed"] += 1

            except Exception as e:
                stats["errors"].append(f"Row {idx}: {str(e)}")
                continue

        # Commit all changes
        db.commit()

        # Clean up temporary file
        os.unlink(tmp_file_path)

        return {
            "success": True,
            "message": "Import completed successfully",
            "statistics": stats
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The Excel file is empty")
    except Exception as e:
        db.rollback()
        # Clean up temporary file if it exists
        if 'tmp_file_path' in locals():
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/status")
def get_import_status(db: Session = Depends(get_db)):
    """Get current database statistics"""
    users_count = db.query(User).count()
    competencies_count = db.query(Competency).count()
    assessments_count = db.query(Assessment).count()

    return {
        "users": users_count,
        "competencies": competencies_count,
        "assessments": assessments_count
    }
