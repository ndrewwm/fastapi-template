"""Entry point for the API."""

import json
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.auth import api_key_auth
from app.database import create_db_and_tables
from app.routes.user import user, users
from app.schemas.message import Message

with open("app/docs/summary.md") as file:
    summary = file.read()

with open("app/docs/description.md") as file:
    description = file.read()

with open("app/docs/tags_metadata.json") as file:
    tags_metadata = json.load(file)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Goodbye!")


app = FastAPI(
    title="Fast API Template",
    version="0.0.1",
    summary=summary,
    description=description,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)
app.include_router(user)
app.include_router(users)


@app.get("/")
async def root(api_key: str = Depends(api_key_auth)) -> Message:
    """API root."""
    return Message(detail="Hello world!")
