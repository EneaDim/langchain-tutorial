from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from common.config import settings
from .routes import files, jobs, health, templates

app = FastAPI(title="SRW API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(files.router, prefix="/v1/files", tags=["files"])
app.include_router(templates.router, prefix="/v1/templates", tags=["templates"])
app.include_router(jobs.router, prefix="/v1/jobs", tags=["jobs"])
