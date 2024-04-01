"""API Key authentication."""

from secrets import token_hex

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pyargon2 import hash
from sqlmodel import Session, select

from app.database import engine
from app.models.user import User

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def api_key_auth(api_key: str = Security(api_key_header)) -> User:
    """Check the request's headers for an API key."""

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key.")

    try:
        key, salt = api_key.split(":")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    hashed = hash_key(key, salt)
    with Session(engine) as session:
        user = session.exec(select(User).where(User.key == hashed)).one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid API key.")

    # TODO: Log the incoming request
    print(f"User: {user.name} ({user.email})")

    return user


async def is_admin(user: str = Depends(api_key_auth)) -> None:
    """Check for elevated permissions."""

    if user.admin != 1:
        raise HTTPException(
            status_code=401, detail="User does not have required permissions."
        )


def hash_key(key: str, salt: str) -> str:
    """Hash a provided API key for storage."""

    return hash(key, salt)


def generate_credentials() -> tuple[int, int, int]:
    """Create a new set of credentials."""

    key = token_hex(24)
    salt = token_hex(30)
    hashed = hash_key(key, salt)
    return key, salt, hashed
