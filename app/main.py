from fastapi import FastAPI

app = FastAPI(
    title="Waypoint Dex",
    description="Project & Decision Manager API",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
