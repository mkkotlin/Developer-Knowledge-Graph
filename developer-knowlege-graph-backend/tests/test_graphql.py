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



