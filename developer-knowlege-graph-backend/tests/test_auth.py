import pytest
from app.graphql.schema import schema
from app.graphql.context import GraphQLContext


@pytest.mark.anyio
async def test_register_and_login_mutations(db_session):
    # Test Register
    reg_mutation = """
        mutation {
            register(username: "dave_ninja", email: "dave@example.com", password: "secret_password", bio: "Fullstack Ninja") {
                token
                user {
                    id
                    username
                    email
                    bio
                }
            }
        }
    """
    res1 = await schema.execute(reg_mutation, context_value=GraphQLContext(db=db_session))
    assert res1.errors is None
    assert res1.data is not None
    reg_data = res1.data["register"]
    assert reg_data["token"] is not None
    assert reg_data["user"]["username"] == "dave_ninja"
    assert reg_data["user"]["email"] == "dave@example.com"

    # Test Login
    login_mutation = """
        mutation {
            login(usernameOrEmail: "dave_ninja", password: "secret_password") {
                token
                user {
                    id
                    username
                }
            }
        }
    """
    res2 = await schema.execute(login_mutation, context_value=GraphQLContext(db=db_session))
    assert res2.errors is None
    assert res2.data is not None
    login_data = res2.data["login"]
    assert login_data["token"] is not None
    assert login_data["user"]["username"] == "dave_ninja"
