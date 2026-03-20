from fastapi import FastAPI

from app.api.auth.router import router as auth_router
from app.api.projects.router import router as projects_router

app = FastAPI(
    title="Waypoint Dex",
    description="Project & Decision Manager API",
    version="0.1.0",
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(projects_router, prefix="/projects", tags=["Projects"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
