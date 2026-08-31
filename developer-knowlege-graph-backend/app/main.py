from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import engine

app = FastAPI(title="Developer Knowledge Graph", version="0.0.1")


@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status":"ok", "database":"connected"}