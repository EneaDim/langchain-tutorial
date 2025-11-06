from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from common.config import settings
from api.routes import files, jobs, health, templates

app = FastAPI(title="SRW API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(templates.router, prefix="/templates", tags=["templates"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
