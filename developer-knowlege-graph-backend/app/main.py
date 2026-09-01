from fastapi import FastAPI
from app.graphql.schema import schema
from strawberry.fastapi import GraphQLRouter


app = FastAPI(title="Developer Knowledge Graph", version="0.0.1")

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
def health_check():
    return {"status":"ok", "database":"connected"}