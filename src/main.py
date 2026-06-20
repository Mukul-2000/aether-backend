from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.api_v1.router import api_router
# 1. Import your database engine and Base class
from src.core.database import engine, Base

# 2. Automatically create all tables defined in your models
def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise-grade autonomous research workflow coordinator.",
    version="1.0.0"
)

# 3. Create tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root_ping():
    return {
        "status": "active",
        "application": settings.PROJECT_NAME,
        "api_v1_entrypoint": f"{settings.API_V1_STR}/docs"
    }