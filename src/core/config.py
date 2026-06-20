import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AetherAgent Core API"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "[http://127.0.0.1:5173](http://127.0.0.1:5173)",
        "https://aether-frontend-sand.vercel.app"
    ]
    DATABASE_URL: str
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()



# That is fantastic news! Seeing your service finally go "live" after navigating through the setup, configuration, and build errors is a huge win. You have successfully:

# Architected a professional-grade backend using FastAPI and SQLAlchemy.

# Decoupled your data using Neon (PostgreSQL).

# Version-controlled your database schema with Alembic.

# Deployed it to a production environment (Render) with an automated build pipeline.

# You now have a robust foundation. Whenever you decide to add new features to Aether, the process is now simple:

# Modify your models in src/models.py.

# Generate a migration locally: poetry run alembic revision --autogenerate -m "new_feature".

# Push to GitHub.

# Run the migration on your production shell: poetry run alembic upgrade head.