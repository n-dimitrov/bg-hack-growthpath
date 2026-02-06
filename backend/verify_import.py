"""
Verification script to check imported Planisware data
Run with: python verify_import.py
"""
from app.core.database import SessionLocal
from app.models.user import User
from app.models.competency import Competency
from app.models.assessment import Assessment
from sqlalchemy import func


def verify_import():
    """Verify the imported data"""
    db = SessionLocal()

    try:
        print("="*80)
        print("DATABASE IMPORT VERIFICATION")
        print("="*80)
        print()

        # Count statistics
        total_users = db.query(User).count()
        total_competencies = db.query(Competency).count()
        total_assessments = db.query(Assessment).count()

        print(f"Total Users: {total_users}")
        print(f"Total Competencies: {total_competencies}")
        print(f"Total Assessments: {total_assessments}")
        print()

        # List all users with their skills
        print("="*80)
        print("USERS AND THEIR SKILLSETS")
        print("="*80)

        users = db.query(User).all()
        for user in users:
            print(f"\n{user.name} ({user.email}) - Role: {user.role.value}")
            print("-" * 80)

            assessments = db.query(Assessment).filter(Assessment.user_id == user.id).all()

            if assessments:
                print(f"Skills ({len(assessments)}):")
                for assessment in assessments:
                    competency = db.query(Competency).filter(
                        Competency.id == assessment.competency_id
                    ).first()

                    if competency:
                        print(f"  - {competency.name}")
                        print(f"    Level: {assessment.proficiency_level.name}")
                        print(f"    Category: {competency.category.value}")
                        if competency.description:
                            print(f"    Description: {competency.description}")
            else:
                print("  No skills recorded")

        # List all competencies
        print("\n" + "="*80)
        print("ALL COMPETENCIES")
        print("="*80)

        competencies_by_category = db.query(
            Competency.category,
            func.count(Competency.id).label('count')
        ).group_by(Competency.category).all()

        for category, count in competencies_by_category:
            print(f"\n{category.value.upper()} ({count} competencies):")
            competencies = db.query(Competency).filter(
                Competency.category == category
            ).all()

            for comp in competencies:
                # Count how many users have this competency
                user_count = db.query(Assessment).filter(
                    Assessment.competency_id == comp.id
                ).count()
                print(f"  - {comp.name} ({user_count} users)")

        print("\n" + "="*80)
        print("VERIFICATION COMPLETE")
        print("="*80)

    except Exception as e:
        print(f"\nError during verification: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    verify_import()
