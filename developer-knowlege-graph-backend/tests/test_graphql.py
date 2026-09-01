import pytest
from app.graphql.schema import schema

def test_developer_query_fixture_data(sample_users, sample_skills, sample_user_skills, monkeypatch, db_session):
    """Test GraphQL query for developer with fixtures."""
    # Override SessionLocal to use the test db_session
    from app.graphql.types import developer
    
    class TestSessionContext:
        def __enter__(self):
            return db_session
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr(developer, "SessionLocal", lambda: TestSessionContext())

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

    result = schema.execute_sync(query)
    assert result.errors is None
    assert result.data is not None
    dev_data = result.data["developer"]
    assert dev_data["username"] == "alice_dev"
    assert dev_data["email"] == "alice@example.com"
    assert len(dev_data["skills"]) == 2
    assert dev_data["skills"][0]["name"] in ["Python Programming", "GraphQL API Design"]
