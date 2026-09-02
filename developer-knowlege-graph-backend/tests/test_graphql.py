import pytest
from app.graphql.schema import schema
from app.graphql.context import GraphQLContext


import pytest
from app.graphql.schema import schema
from app.graphql.context import GraphQLContext


@pytest.mark.anyio
async def test_developer_query_fixture_data(sample_users, sample_skills, sample_user_skills, db_session):
    """Test GraphQL query for developer with fixtures."""
    query = """
        query GetDeveloper {
            developer(id: %d) {
                id
                username
                email
                bio
                skills {
                    id
                    name
                    proficiency
                }
            }
        }
    """ % sample_users[0].id

    result = await schema.execute(query, context_value=GraphQLContext(db=db_session))
    assert result.errors is None
    assert result.data is not None
    dev_data = result.data["developer"]
    assert dev_data["username"] == "alice_dev"
    assert dev_data["email"] == "alice@example.com"
    assert len(dev_data["skills"]) == 2
    assert dev_data["skills"][0]["name"] in ["Python Programming", "GraphQL API Design"]


@pytest.mark.anyio
async def test_project_skills_query(sample_users, sample_skills, db_session):
    """Test GraphQL query for developer projects and project skills."""
    from app.models.project import Project
    from app.models.project_skill import ProjectSkill

    project = Project(name="Knowledge Graph", description="Backend service", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    proj_skill = ProjectSkill(project_id=project.id, skill_id=sample_skills[0].id, proficiency_demonstrated=4)
    db_session.add(proj_skill)
    db_session.commit()

    query = """
        query GetDeveloperProjects {
            developer(id: %d) {
                projects {
                    id
                    name
                    skills {
                        id
                        name
                        proficiency
                    }
                }
            }
        }
    """ % sample_users[0].id

    result = await schema.execute(query, context_value=GraphQLContext(db=db_session))
    assert result.errors is None
    assert result.data is not None
    projects = result.data["developer"]["projects"]
    assert len(projects) == 1
    assert projects[0]["name"] == "Knowledge Graph"
    assert len(projects[0]["skills"]) == 1
    assert projects[0]["skills"][0]["name"] == "Python Programming"
    assert projects[0]["skills"][0]["proficiency"] == 0



@pytest.mark.anyio
async def test_create_skill_mutation(db_session):
    """Test create_skill mutation with GraphQLContext."""
    mutation = """
        mutation {
            createSkill(name: "Rust", description: "Systems programming") {
                id
                name
                description
            }
        }
    """
    result = await schema.execute(mutation, context_value=GraphQLContext(db=db_session))
    assert result.errors is None
    assert result.data["createSkill"]["name"] == "Rust"


@pytest.mark.anyio
async def test_developer_technology_category_traversal(sample_users, db_session):
    """Test complete traversal: Developer -> Project -> Technology -> TechnologyCategory."""
    from app.models.project import Project
    from app.models.technology_category import TechnologyCategory
    from app.models.technology import Technology
    from app.models.project_technology import ProjectTechnology

    category = TechnologyCategory(name="Backend Framework", description="Frameworks for backend dev")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    tech = Technology(name="FastAPI", description="Python Web Framework", category_id=category.id)
    db_session.add(tech)
    db_session.commit()
    db_session.refresh(tech)

    project = Project(name="Developer Knowledge Graph", description="Backend service", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    proj_tech = ProjectTechnology(project_id=project.id, technology_id=tech.id)
    db_session.add(proj_tech)
    db_session.commit()

    query = """
        query GetDeveloperTraversal {
            developer(id: %d) {
                username
                projects {
                    name
                    technologies {
                        name
                        category {
                            name
                            description
                        }
                    }
                }
            }
        }
    """ % sample_users[0].id

    result = await schema.execute(query, context_value=GraphQLContext(db=db_session))
    assert result.errors is None
    assert result.data is not None
    dev = result.data["developer"]
    assert dev["username"] == "alice_dev"
    assert len(dev["projects"]) == 1
    assert dev["projects"][0]["name"] == "Developer Knowledge Graph"
    assert len(dev["projects"][0]["technologies"]) == 1
    tech_data = dev["projects"][0]["technologies"][0]
    assert tech_data["name"] == "FastAPI"
    assert tech_data["category"]["name"] == "Backend Framework"
    assert tech_data["category"]["description"] == "Frameworks for backend dev"


@pytest.mark.anyio
async def test_developers_filter_query(sample_users, sample_skills, sample_user_skills, db_session):
    """Test developers query with skill filter."""
    query = """
        query {
            developers(filter: { skills: ["Python Programming"], minProficiency: 4 }) {

                edges {
                    cursor
                    node {
                        id
                        username
                        skills {
                            name
                            proficiency
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """
    result = await schema.execute(query, context_value=GraphQLContext(db=db_session))
    assert result.errors is None
    assert result.data is not None
    connection = result.data["developers"]
    assert len(connection["edges"]) == 1
    node = connection["edges"][0]["node"]
    assert node["username"] == "alice_dev"



@pytest.mark.anyio
async def test_projects_filter_query(sample_users, db_session):
    """Test projects query with technology filter."""
    from app.models.project import Project
    from app.models.technology_category import TechnologyCategory
    from app.models.technology import Technology
    from app.models.project_technology import ProjectTechnology

    category = TechnologyCategory(name="Backend Framework", description="Frameworks for backend dev")
    db_session.add(category)
    db_session.commit()

    tech = Technology(name="FastAPI", description="Python Web Framework", category_id=category.id)
    db_session.add(tech)
    db_session.commit()

    project = Project(name="Knowledge Graph", description="Backend service", status="active", owner_id=sample_users[0].id)
    db_session.add(project)
    db_session.commit()

    proj_tech = ProjectTechnology(project_id=project.id, technology_id=tech.id)
    db_session.add(proj_tech)
    db_session.commit()

    query = """
        query {
            projects(filter: { technology: "FastAPI" }) {
                edges {
                    cursor
                    node {
                        id
                        name
                        technologies {
                            name
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """
    result = await schema.execute(query, context_value=GraphQLContext(db=db_session))
    assert result.errors is None
    assert result.data is not None
    connection = result.data["projects"]
    assert len(connection["edges"]) == 1
    node = connection["edges"][0]["node"]
    assert node["name"] == "Knowledge Graph"
    assert node["technologies"][0]["name"] == "FastAPI"


@pytest.mark.anyio
async def test_projects_pagination_query(sample_users, db_session):
    """Test cursor-based pagination for projects query across pages."""
    from app.models.project import Project

    p1 = Project(name="Project 1", description="P1", status="active", owner_id=sample_users[0].id)
    p2 = Project(name="Project 2", description="P2", status="active", owner_id=sample_users[0].id)
    p3 = Project(name="Project 3", description="P3", status="active", owner_id=sample_users[0].id)
    db_session.add_all([p1, p2, p3])
    db_session.commit()

    # Query Page 1 (first: 2)
    query_page1 = """
        query {
            projects(first: 2) {
                edges {
                    cursor
                    node {
                        id
                        name
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """
    res1 = await schema.execute(query_page1, context_value=GraphQLContext(db=db_session))
    assert res1.errors is None
    data1 = res1.data["projects"]
    assert len(data1["edges"]) == 2
    assert data1["pageInfo"]["hasNextPage"] is True
    end_cursor = data1["pageInfo"]["endCursor"]
    assert end_cursor is not None

    # Query Page 2 (first: 2, after: end_cursor)
    query_page2 = """
        query {
            projects(first: 2, after: "%s") {
                edges {
                    cursor
                    node {
                        id
                        name
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """ % end_cursor
    res2 = await schema.execute(query_page2, context_value=GraphQLContext(db=db_session))
    assert res2.errors is None
    data2 = res2.data["projects"]
    assert len(data2["edges"]) == 1
    assert data2["pageInfo"]["hasNextPage"] is False