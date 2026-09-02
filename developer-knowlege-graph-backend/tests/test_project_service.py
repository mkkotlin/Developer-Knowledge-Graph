import pytest
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService
from app.models.project import Project
from app.models.technology_category import TechnologyCategory
from app.models.technology import Technology
from app.models.project_technology import ProjectTechnology
from app.models.project_skill import ProjectSkill


@pytest.mark.anyio
async def test_project_repository_find_by_id(sample_users, db_session):
    project = Project(name="Test Project", description="Test Desc", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    repo = ProjectRepository(db_session)
    found = await repo.find_by_id(project.id)
    assert found is not None
    assert found.name == "Test Project"


@pytest.mark.anyio
async def test_project_service_find_by_technology(sample_users, db_session):
    category = TechnologyCategory(name="Database", description="Data stores")
    db_session.add(category)
    db_session.commit()

    tech = Technology(name="PostgreSQL", description="Relational DB", category_id=category.id)
    db_session.add(tech)
    db_session.commit()

    project = Project(name="DB Project", description="Database service", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()

    proj_tech = ProjectTechnology(project_id=project.id, technology_id=tech.id)
    db_session.add(proj_tech)
    db_session.commit()

    service = ProjectService(db_session)
    
    # Test empty name validation
    empty_result = await service.find_by_technology("   ")
    assert empty_result == []

    # Test technology search
    projects = await service.find_by_technology("PostgreSQL")
    assert len(projects) == 1
    assert projects[0].name == "DB Project"


@pytest.mark.anyio
async def test_project_service_find_by_skill(sample_users, sample_skills, db_session):
    project = Project(name="Python App", description="Python service", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()

    proj_skill = ProjectSkill(project_id=project.id, skill_id=sample_skills[0].id, proficiency_demonstrated=5)
    db_session.add(proj_skill)
    db_session.commit()

    service = ProjectService(db_session)

    # Test empty name validation
    empty_result = await service.find_by_skill("   ")
    assert empty_result == []

    # Test skill search
    projects = await service.find_by_skill("Python Programming")
    assert len(projects) == 1
    assert projects[0].name == "Python App"

    # Test list_projects
    all_projects = await service.list_projects()
    assert len(all_projects) == 1


@pytest.mark.anyio
async def test_project_service_search_combined(sample_users, sample_skills, db_session):
    category = TechnologyCategory(name="Framework", description="Web Frameworks")
    db_session.add(category)
    db_session.commit()

    tech = Technology(name="FastAPI", description="Python Framework", category_id=category.id)
    db_session.add(tech)
    db_session.commit()

    project = Project(name="Knowledge Graph App", description="KG service", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()

    proj_tech = ProjectTechnology(project_id=project.id, technology_id=tech.id)
    proj_skill = ProjectSkill(project_id=project.id, skill_id=sample_skills[0].id, proficiency_demonstrated=5)
    db_session.add_all([proj_tech, proj_skill])
    db_session.commit()

    service = ProjectService(db_session)
    results = await service.search(first=10, technology="FastAPI", skill="Python Programming")
    assert len(results) == 1
    assert results[0].name == "Knowledge Graph App"


