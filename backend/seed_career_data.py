"""Seed database with career framework and skills data"""
import json
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal, engine, Base
from app.models.career import (
    CareerLevel,
    CompetencyArea,
    CompetencyExpectation,
    Skill
)


def load_json_file(filename):
    """Load JSON file from project root"""
    file_path = Path(__file__).parent.parent / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_career_framework(db):
    """Seed career levels and competencies"""
    print("📊 Seeding Career Framework...")

    framework = load_json_file('CareerFramework.json')

    # Seed career levels
    level_count = 0
    for track_key, track_data in framework['career_tracks'].items():
        for level_data in track_data['levels']:
            career_level = CareerLevel(
                track=track_key,
                level=level_data['level'],
                title=level_data['title'],
                pay_class=level_data['pay_class'],
                summary=level_data['summary'],
                impact_scope=level_data['impact_scope'],
                project_category=level_data.get('project_category')
            )
            db.add(career_level)
            level_count += 1

    print(f"  ✓ Added {level_count} career levels")

    # Seed competency areas
    comp_count = 0
    expect_count = 0
    for area_key, area_data in framework['competency_areas'].items():
        competency = CompetencyArea(
            area_key=area_key,
            name=area_data['name'],
            description=area_data['description']
        )
        db.add(competency)
        db.flush()  # Get the ID
        comp_count += 1

        # Seed expectations per level
        for pay_class, level_data in area_data['levels'].items():
            expectation = CompetencyExpectation(
                competency_area_id=competency.id,
                pay_class=pay_class,
                expectations=level_data['expectations'],
                scope=level_data.get('scope')
            )
            db.add(expectation)
            expect_count += 1

    print(f"  ✓ Added {comp_count} competency areas")
    print(f"  ✓ Added {expect_count} competency expectations")

    # Seed architect competencies
    arch_comp_count = 0
    arch_expect_count = 0
    for area_key, area_data in framework['architect_competencies'].items():
        competency = CompetencyArea(
            area_key=f"architect_{area_key}",
            name=area_data['name'],
            description=area_data['description']
        )
        db.add(competency)
        db.flush()
        arch_comp_count += 1

        # Add architect-specific expectations
        for level_key in ['architect', 'senior_architect']:
            if level_key in area_data:
                level_data = area_data[level_key]
                expectation = CompetencyExpectation(
                    competency_area_id=competency.id,
                    pay_class=level_data['pay_class'],
                    expectations=level_data['expectations']
                )
                db.add(expectation)
                arch_expect_count += 1

        # Handle shared expectations
        if 'shared' in area_data:
            for pay_class in ['PC09', 'PC10']:
                expectation = CompetencyExpectation(
                    competency_area_id=competency.id,
                    pay_class=pay_class,
                    expectations=area_data['shared']['expectations']
                )
                db.add(expectation)
                arch_expect_count += 1

    print(f"  ✓ Added {arch_comp_count} architect competencies")
    print(f"  ✓ Added {arch_expect_count} architect expectations")


def seed_skills(db):
    """Seed skills from TechMasterData and Skillsets"""
    print("\n🔧 Seeding Skills...")

    # Seed from TechMasterData.json
    tech_data = load_json_file('TechMasterData.json')
    tech_count = 0

    for item in tech_data['flat']:
        skill = Skill(
            name=item['sub_skill'],
            parent_category=item['parent_skill'],
            description=item['full_name'],
            is_data_skill=0
        )
        db.add(skill)
        tech_count += 1

    print(f"  ✓ Added {tech_count} technology skills from TechMasterData")

    # Seed from Skillsets.json (data-focused skills)
    skillsets_data = load_json_file('Skillsets.json')
    skillset_count = 0

    for skillset in skillsets_data['skillsets']:
        skill = Skill(
            name=skillset['name'],
            parent_category='Data',
            description=skillset.get('description', ''),
            category=skillset.get('category', 'Standard'),
            roles=skillset.get('roles', ''),
            is_data_skill=1
        )
        db.add(skill)
        skillset_count += 1

    print(f"  ✓ Added {skillset_count} data skillsets from Skillsets")


def main():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 GrowthPath Database Seeding")
    print("=" * 60)

    # Create tables
    print("\n📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("  ✓ Tables created")

    # Create session
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_levels = db.query(CareerLevel).count()
        if existing_levels > 0:
            print("\n⚠️  Database already contains data!")
            response = input("Do you want to clear and re-seed? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled")
                return

            # Clear existing data
            print("\n🗑️  Clearing existing data...")
            db.query(LearningObjective).delete()
            db.query(DevelopmentPlan).delete()
            db.query(UserSkill).delete()
            db.query(Skill).delete()
            db.query(CompetencyExpectation).delete()
            db.query(CompetencyArea).delete()
            db.query(CareerLevel).delete()
            db.commit()
            print("  ✓ Data cleared")

        # Seed data
        seed_career_framework(db)
        seed_skills(db)

        # Commit all changes
        db.commit()

        # Show statistics
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        print(f"\nStatistics:")
        print(f"  Career Levels: {db.query(CareerLevel).count()}")
        print(f"  Competency Areas: {db.query(CompetencyArea).count()}")
        print(f"  Competency Expectations: {db.query(CompetencyExpectation).count()}")
        print(f"  Skills: {db.query(Skill).count()}")
        print("\n🚀 Your GrowthPath database is ready to use!")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Import LearningObjective here to avoid circular import
    from app.models.career import LearningObjective
    main()
