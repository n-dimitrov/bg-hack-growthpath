"""
Import script for Planisware employee tagging data
Imports employees and their skillsets from Excel file into the database
Run with: python import_plw_data.py
"""
import pandas as pd
from passlib.context import CryptContext
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.competency import Competency, CompetencyCategory
from app.models.assessment import Assessment, ProficiencyLevel

# Create tables
Base.metadata.create_all(bind=engine)

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


def import_plw_data(excel_file: str):
    """Import employee data from Planisware Excel file"""
    db = SessionLocal()

    try:
        # Read the Excel file
        print(f"Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)

        print(f"Found {len(df)} records in Excel file")
        print(f"Columns: {df.columns.tolist()}\n")

        # Track statistics
        users_created = 0
        users_existing = 0
        competencies_created = 0
        competencies_existing = 0
        assessments_created = 0

        # Process each row
        for idx, row in df.iterrows():
            # Extract data
            name = row['Name']
            skillset = row['Skillset']
            skillset_level = row['Skillset Level']
            location = row.get('Resource Location', '')
            country = row.get('Resource Country', '')
            region = row.get('Resource Region', '')
            description = row.get('Skillsets.Description', '')
            category = row.get('Skillsets.Category', '')
            role = row.get('Skillsets.Role', '')

            # Skip if essential data is missing
            if pd.isna(name) or pd.isna(skillset):
                print(f"Row {idx}: Skipping - missing name or skillset")
                continue

            # Create/Get User
            # Generate email from name
            email = name.lower().replace(' ', '.') + '@bosch.com'

            user = db.query(User).filter(User.email == email).first()
            if not user:
                # Create new user
                user = User(
                    email=email,
                    name=name,
                    role=UserRole.EMPLOYEE,
                    hashed_password=pwd_context.hash('password123')  # Default password
                )
                db.add(user)
                db.flush()  # Get the user ID
                users_created += 1
                print(f"Created user: {name} ({email})")
            else:
                users_existing += 1

            # Create/Get Competency
            competency = db.query(Competency).filter(Competency.name == skillset).first()
            if not competency:
                # Create new competency
                comp_category = map_category_to_competency_category(category)
                competency = Competency(
                    name=skillset,
                    description=description if not pd.isna(description) else None,
                    category=comp_category
                )
                db.add(competency)
                db.flush()  # Get the competency ID
                competencies_created += 1
                print(f"Created competency: {skillset} ({comp_category.value})")
            else:
                competencies_existing += 1

            # Create Assessment (link user to competency with proficiency level)
            proficiency = map_skillset_level_to_proficiency(skillset_level)

            # Check if assessment already exists
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
                assessments_created += 1
                print(f"Created assessment: {name} -> {skillset} ({proficiency.name})")
            else:
                print(f"Assessment already exists: {name} -> {skillset} ({proficiency.name})")

        # Commit all changes
        db.commit()

        # Print summary
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"Users created: {users_created}")
        print(f"Users existing: {users_existing}")
        print(f"Competencies created: {competencies_created}")
        print(f"Competencies existing: {competencies_existing}")
        print(f"Assessments created: {assessments_created}")
        print("="*60)
        print("\nImport completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"\nError during import: {str(e)}")
        raise
    finally:
        db.close()


def cleanup_data():
    """Clean up all imported data (for testing)"""
    db = SessionLocal()

    try:
        print("Cleaning up data...")

        # Delete all assessments
        assessments_deleted = db.query(Assessment).delete()
        print(f"Deleted {assessments_deleted} assessments")

        # Delete all users
        users_deleted = db.query(User).delete()
        print(f"Deleted {users_deleted} users")

        # Delete all competencies
        competencies_deleted = db.query(Competency).delete()
        print(f"Deleted {competencies_deleted} competencies")

        db.commit()
        print("\nCleanup completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"\nError during cleanup: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    # Get file path from command line or use default
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cleanup":
            print("="*60)
            print("CLEANUP DATA")
            print("="*60)
            print()
            cleanup_data()
            sys.exit(0)
        else:
            excel_file = sys.argv[1]
    else:
        excel_file = "../plw_employee_taging-test.xlsx"

    print("="*60)
    print("PLANISWARE EMPLOYEE DATA IMPORT")
    print("="*60)
    print()

    import_plw_data(excel_file)
