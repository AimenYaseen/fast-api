from functools import lru_cache

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated


# create the env and set these variables there
class Settings(BaseSettings):
    app_name: str = "VARIABLE APP"
    admin_email: str = ""
    items_per_user: int = 50

    model_config = SettingsConfigDict(env_file=".env")


app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
