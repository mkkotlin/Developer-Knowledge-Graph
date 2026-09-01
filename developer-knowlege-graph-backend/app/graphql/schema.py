import strawberry
from app.graphql.types.developer import DeveloperQuery


@strawberry.type
class Query(DeveloperQuery):

    @strawberry.field
    def hello(self) -> str:
        return "Developer Knowledge Graph"

schema = strawberry.Schema(query=Query)