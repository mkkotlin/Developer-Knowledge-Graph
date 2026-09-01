import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models import User, Skill, UserSkill, TechnologyCategory, Technology, Project

# In-memory SQLite database engine for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Fixture to provide a clean SQLite database session for each test."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def sample_users(db_session):
    """Fixture providing 3 sample user records."""
    users = [
        User(
            username="alice_dev",
            email="alice@example.com",
            password_hash="pass_1",
            bio="Backend developer",
        ),
        User(
            username="bob_coder",
            email="bob@example.com",
            password_hash="pass_2",
            bio="Frontend developer",
        ),
        User(
            username="charlie_architect",
            email="charlie@example.com",
            password_hash="pass_3",
            bio="DevOps architect",
        ),
    ]
    db_session.add_all(users)
    db_session.commit()
    for u in users:
        db_session.refresh(u)
    return users


@pytest.fixture(scope="function")
def sample_skills(db_session):
    """Fixture providing 3 sample skill records."""
    skills = [
        Skill(name="Python Programming", description="Core Python skills"),
        Skill(name="GraphQL API Design", description="GraphQL schemas with Strawberry"),
        Skill(name="Database Modeling", description="Relational DB design"),
    ]
    db_session.add_all(skills)
    db_session.commit()
    for s in skills:
        db_session.refresh(s)
    return skills


@pytest.fixture(scope="function")
def sample_user_skills(db_session, sample_users, sample_skills):
    """Fixture linking users to skills with proficiencies (3 records)."""
    user_skills = [
        UserSkill(user_id=sample_users[0].id, skill_id=sample_skills[0].id, proficiency=5),
        UserSkill(user_id=sample_users[0].id, skill_id=sample_skills[1].id, proficiency=4),
        UserSkill(user_id=sample_users[1].id, skill_id=sample_skills[0].id, proficiency=3),
    ]
    db_session.add_all(user_skills)
    db_session.commit()
    return user_skills
