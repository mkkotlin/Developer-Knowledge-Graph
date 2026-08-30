from fastapi import FastAPI

app = FastAPI(title="Developer Knowledge Graph", version="0.0.1")


@app.get("/health")
def health_check():
    return {"status":"ok"}