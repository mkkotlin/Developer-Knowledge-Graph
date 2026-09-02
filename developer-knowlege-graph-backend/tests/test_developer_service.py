import pytest
from app.repositories.developer_repository import DeveloperRepository
from app.services.developer_service import DeveloperService


@pytest.mark.anyio
async def test_developer_repository_find_by_id(sample_users, db_session):
    repo = DeveloperRepository(db_session)
    user = await repo.find_by_id(sample_users[0].id)
    assert user is not None
    assert user.username == "alice_dev"


@pytest.mark.anyio
async def test_developer_repository_find_by_skill(sample_users, sample_skills, sample_user_skills, db_session):
    repo = DeveloperRepository(db_session)
    users = await repo.find_by_skill("Python Programming", min_proficiency=4)
    assert len(users) == 1
    assert users[0].username == "alice_dev"


@pytest.mark.anyio
async def test_developer_service(sample_users, sample_skills, sample_user_skills, db_session):
    service = DeveloperService(db_session)
    
    # Test empty skill name business logic
    empty_result = await service.find_developers_by_skill("   ")
    assert empty_result == []

    # Test valid skill query
    devs = await service.find_developers_by_skill("Python Programming")
    assert len(devs) == 2

    # Test list_developers
    all_devs = await service.list_developers()
    assert len(all_devs) == 3

    # Test search method with project_technology multi-hop
    from app.models.project import Project
    from app.models.technology_category import TechnologyCategory
    from app.models.technology import Technology
    from app.models.project_technology import ProjectTechnology

    cat = TechnologyCategory(name="Framework", description="Web Frameworks")
    db_session.add(cat)
    db_session.commit()

    tech = Technology(name="FastAPI", description="Python Framework", category_id=cat.id)
    db_session.add(tech)
    db_session.commit()

    proj = Project(name="KG Backend", description="Backend service", status="active", owner_id=sample_users[0].id)
    db_session.add(proj)
    db_session.commit()

    proj_tech = ProjectTechnology(project_id=proj.id, technology_id=tech.id)
    db_session.add(proj_tech)
    db_session.commit()

    multihop_devs = await service.search(first=10, skills=["Python Programming"], min_proficiency=4, technologies=["FastAPI"])
    assert len(multihop_devs) == 1
    assert multihop_devs[0].username == "alice_dev"




