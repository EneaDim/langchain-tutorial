from fastapi import FastAPI
from fastapi.responses import JSONResponse

def create_app() -> FastAPI:
    app = FastAPI(title="Smart Report Writer API", version="0.1.0")

    @app.get("/healthz")
    def healthz():
        return JSONResponse({"status": "ok"})

    # Mount your real routes here when ready:
    # from .routes_uploads import router as uploads
    # app.include_router(uploads, prefix="/v1")
    return app

# Uvicorn can import either create_app (factory) or app (instance)
app = create_app()
