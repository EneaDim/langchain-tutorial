from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.jobs import router as jobs_router
from app.api.v1.routes.analyze import router as analyze_router

app = FastAPI(title="AI-Doc Analyzer API", version="1.0.0", openapi_url="/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# Mount v1
app.include_router(health_router, prefix="/api/v1")
app.include_router(jobs_router,   prefix="/api/v1")
app.include_router(analyze_router, prefix="/api/v1")

# Back-compat minimal
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
