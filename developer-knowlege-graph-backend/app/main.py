from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.graphql.context import get_context
from app.graphql.error_formatter import format_error
from app.graphql.schema import schema


class CustomGraphQLRouter(GraphQLRouter):
    async def process_result(self, request, result):
        data = await super().process_result(request, result)
        if result.errors:
            data["errors"] = [format_error(err) for err in result.errors]
        return data


app = FastAPI(
    title="Developer Knowledge Graph",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



graphql_app = CustomGraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(
    graphql_app,
    prefix="/graphql",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

