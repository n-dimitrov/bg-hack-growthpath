"""
Seed script to populate the database with sample competencies
Run with: python seed_data.py
"""
from app.core.database import SessionLocal, engine, Base
from app.models.competency import Competency, CompetencyCategory

# Create tables
Base.metadata.create_all(bind=engine)

def seed_competencies():
    db = SessionLocal()

    # Check if data already exists
    existing = db.query(Competency).first()
    if existing:
        print("Database already contains competencies. Skipping seed.")
        db.close()
        return

    sample_competencies = [
        # Technical Skills
        {
            "name": "Python Programming",
            "description": "Proficiency in Python language, libraries, and best practices",
            "category": CompetencyCategory.TECHNICAL
        },
        {
            "name": "Web Development",
            "description": "Frontend and backend web development skills (HTML, CSS, JavaScript, frameworks)",
            "category": CompetencyCategory.TECHNICAL
        },
        {
            "name": "Database Management",
            "description": "SQL, NoSQL, database design and optimization",
            "category": CompetencyCategory.TECHNICAL
        },
        {
            "name": "Cloud Technologies",
            "description": "AWS, Azure, GCP - cloud infrastructure and services",
            "category": CompetencyCategory.TECHNICAL
        },
        {
            "name": "DevOps & CI/CD",
            "description": "Continuous integration, deployment pipelines, Docker, Kubernetes",
            "category": CompetencyCategory.TECHNICAL
        },

        # Soft Skills
        {
            "name": "Communication",
            "description": "Clear verbal and written communication with team members and stakeholders",
            "category": CompetencyCategory.SOFT_SKILLS
        },
        {
            "name": "Problem Solving",
            "description": "Analytical thinking and creative solution development",
            "category": CompetencyCategory.SOFT_SKILLS
        },
        {
            "name": "Collaboration",
            "description": "Working effectively in team environments, cross-functional cooperation",
            "category": CompetencyCategory.SOFT_SKILLS
        },
        {
            "name": "Time Management",
            "description": "Prioritization, meeting deadlines, managing multiple tasks",
            "category": CompetencyCategory.SOFT_SKILLS
        },
        {
            "name": "Adaptability",
            "description": "Flexibility in changing environments, learning new technologies",
            "category": CompetencyCategory.SOFT_SKILLS
        },

        # Leadership
        {
            "name": "Team Leadership",
            "description": "Leading and motivating teams, delegating tasks effectively",
            "category": CompetencyCategory.LEADERSHIP
        },
        {
            "name": "Strategic Thinking",
            "description": "Long-term planning, identifying opportunities and risks",
            "category": CompetencyCategory.LEADERSHIP
        },
        {
            "name": "Decision Making",
            "description": "Making informed decisions under pressure and uncertainty",
            "category": CompetencyCategory.LEADERSHIP
        },
        {
            "name": "Mentoring",
            "description": "Coaching and developing team members, knowledge sharing",
            "category": CompetencyCategory.LEADERSHIP
        },

        # Domain Knowledge
        {
            "name": "Agile Methodologies",
            "description": "Scrum, Kanban, agile principles and practices",
            "category": CompetencyCategory.DOMAIN_KNOWLEDGE
        },
        {
            "name": "Software Architecture",
            "description": "System design patterns, microservices, scalability principles",
            "category": CompetencyCategory.DOMAIN_KNOWLEDGE
        },
        {
            "name": "Data Analysis",
            "description": "Data interpretation, statistical analysis, visualization",
            "category": CompetencyCategory.DOMAIN_KNOWLEDGE
        },
        {
            "name": "Security Best Practices",
            "description": "Application security, authentication, encryption, compliance",
            "category": CompetencyCategory.DOMAIN_KNOWLEDGE
        }
    ]

    for comp_data in sample_competencies:
        competency = Competency(**comp_data)
        db.add(competency)

    db.commit()
    print(f"Successfully seeded {len(sample_competencies)} competencies!")
    db.close()

if __name__ == "__main__":
    seed_competencies()
