"""
Data Seeding Module for Developer Knowledge Graph.
Contains fixtures/seed data for Users, Skills, UserSkills, Technologies, and Projects.
"""

from app.db.database import SessionLocal, engine, Base
from app.models import (
    User,
    Skill,
    UserSkill,
    TechnologyCategory,
    Technology,
    Project,
    ProjectTechnology,
    ProjectSkill,
)

# -----------------------------------------------------------------------------
# Seed Fixture Data (3 items for each entity)
# -----------------------------------------------------------------------------

USERS_FIXTURES = [
    {
        "username": "alice_dev",
        "email": "alice@example.com",
        "password_hash": "pbkdf2:sha256:hashed_password_1",
        "bio": "Senior Backend Engineer working with Python, FastAPI & GraphQL",
    },
    {
        "username": "bob_coder",
        "email": "bob@example.com",
        "password_hash": "pbkdf2:sha256:hashed_password_2",
        "bio": "Frontend & Fullstack Developer specializing in React & TypeScript",
    },
    {
        "username": "charlie_architect",
        "email": "charlie@example.com",
        "password_hash": "pbkdf2:sha256:hashed_password_3",
        "bio": "Cloud Architect & DevOps Specialist focused on Kubernetes & Docker",
    },
]

SKILLS_FIXTURES = [
    {
        "name": "Python Programming",
        "description": "Core Python, async programming, and backend framework development",
    },
    {
        "name": "GraphQL API Design",
        "description": "Designing efficient schemas, queries, and mutations with Strawberry & FastAPI",
    },
    {
        "name": "Database Modeling",
        "description": "Relational schema design, SQL optimization, and ORMs with SQLAlchemy",
    },
]

TECH_CATEGORIES_FIXTURES = [
    {
        "name": "Languages & Frameworks",
        "description": "Programming languages, web frameworks, and application runtime libraries",
    },
    {
        "name": "Databases",
        "description": "Relational and NoSQL database management systems and data stores",
    },
    {
        "name": "DevOps & Cloud",
        "description": "Infrastructure, containerization platforms, and deployment tools",
    },
]

TECHNOLOGIES_FIXTURES = [
    {
        "name": "FastAPI",
        "description": "Modern, fast web framework for building APIs with Python",
        "category_index": 0,
    },
    {
        "name": "PostgreSQL",
        "description": "Advanced open source relational database system",
        "category_index": 1,
    },
    {
        "name": "Docker",
        "description": "Containerization platform for packaging and deploying applications",
        "category_index": 2,
    },
]

PROJECTS_FIXTURES = [
    {
        "name": "Developer Knowledge Graph",
        "description": "GraphQL backend service for developer skill graphs and talent discovery",
        "status": "ACTIVE",
        "owner_index": 0,
    },
    {
        "name": "DevOps Pipeline Automation",
        "description": "Automated CI/CD infrastructure and containerized workflow system",
        "status": "ACTIVE",
        "owner_index": 2,
    },
    {
        "name": "Interactive Dashboard",
        "description": "Fullstack web application for monitoring team skills and analytics",
        "status": "COMPLETED",
        "owner_index": 1,
    },
]


def seed_database():
    """Seed database with 3 sample fixture records for each entity."""
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        print("Seeding Users...")
        created_users = []
        for u_data in USERS_FIXTURES:
            user = db.query(User).filter_by(username=u_data["username"]).first()
            if not user:
                user = User(**u_data)
                db.add(user)
                db.flush()
            created_users.append(user)

        print("Seeding Skills...")
        created_skills = []
        for s_data in SKILLS_FIXTURES:
            skill = db.query(Skill).filter_by(name=s_data["name"]).first()
            if not skill:
                skill = Skill(**s_data)
                db.add(skill)
                db.flush()
            created_skills.append(skill)

        print("Seeding UserSkills...")
        user_skills_specs = [
            (0, 0, 5),  # Alice -> Python (5)
            (0, 1, 4),  # Alice -> GraphQL (4)
            (0, 2, 4),  # Alice -> DB (4)
            (1, 0, 3),  # Bob -> Python (3)
            (1, 1, 5),  # Bob -> GraphQL (5)
            (2, 2, 5),  # Charlie -> DB (5)
        ]
        for u_idx, s_idx, prof in user_skills_specs:
            existing = (
                db.query(UserSkill)
                .filter_by(
                    user_id=created_users[u_idx].id,
                    skill_id=created_skills[s_idx].id,
                )
                .first()
            )
            if not existing:
                db.add(
                    UserSkill(
                        user_id=created_users[u_idx].id,
                        skill_id=created_skills[s_idx].id,
                        proficiency=prof,
                    )
                )

        print("Seeding Technology Categories...")
        created_categories = []
        for c_data in TECH_CATEGORIES_FIXTURES:
            cat = db.query(TechnologyCategory).filter_by(name=c_data["name"]).first()
            if not cat:
                cat = TechnologyCategory(**c_data)
                db.add(cat)
                db.flush()
            created_categories.append(cat)

        print("Seeding Technologies...")
        created_techs = []
        for t_data in TECHNOLOGIES_FIXTURES:
            tech = db.query(Technology).filter_by(name=t_data["name"]).first()
            if not tech:
                tech = Technology(
                    name=t_data["name"],
                    description=t_data["description"],
                    category_id=created_categories[t_data["category_index"]].id,
                )
                db.add(tech)
                db.flush()
            created_techs.append(tech)

        print("Seeding Projects...")
        created_projects = []
        for p_data in PROJECTS_FIXTURES:
            proj = db.query(Project).filter_by(name=p_data["name"]).first()
            if not proj:
                proj = Project(
                    name=p_data["name"],
                    description=p_data["description"],
                    status=p_data["status"],
                    owner_id=created_users[p_data["owner_index"]].id,
                )
                db.add(proj)
                db.flush()
            created_projects.append(proj)

        print("Seeding Project Skills & Technologies...")
        # Project 0 -> Skill 0, Skill 1, Tech 0, Tech 1
        # Project 1 -> Skill 2, Tech 2
        # Project 2 -> Skill 1, Tech 0
        p_skill_specs = [(0, 0, 5), (0, 1, 4), (1, 2, 5), (2, 1, 4)]
        for p_idx, s_idx, prof in p_skill_specs:
            existing = (
                db.query(ProjectSkill)
                .filter_by(
                    project_id=created_projects[p_idx].id,
                    skill_id=created_skills[s_idx].id,
                )
                .first()
            )
            if not existing:
                db.add(
                    ProjectSkill(
                        project_id=created_projects[p_idx].id,
                        skill_id=created_skills[s_idx].id,
                        proficiency_demonstrated=prof,
                    )
                )

        p_tech_specs = [(0, 0), (0, 1), (1, 2), (2, 0)]
        for p_idx, t_idx in p_tech_specs:
            existing = (
                db.query(ProjectTechnology)
                .filter_by(
                    project_id=created_projects[p_idx].id,
                    technology_id=created_techs[t_idx].id,
                )
                .first()
            )
            if not existing:
                db.add(
                    ProjectTechnology(
                        project_id=created_projects[p_idx].id,
                        technology_id=created_techs[t_idx].id,
                    )
                )

        db.commit()
        print("Database seeded successfully with 3 fixture items for each entity!")


if __name__ == "__main__":
    seed_database()
