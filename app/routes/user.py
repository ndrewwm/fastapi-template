"""User CRUD."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.auth import generate_credentials, is_admin
from app.database import engine
from app.models.user import User
from app.schemas.message import Message
from app.schemas.user import NewUserInput, NewUserResponse, UserResponse

RESPONSES = {
    400: {"model": Message},
    401: {"model": Message},
    404: {"model": Message},
    405: {"model": Message},
}

user = APIRouter(prefix="/user", tags=["User"], responses=RESPONSES)
users = APIRouter(prefix="/users", tags=["User"], responses=RESPONSES)


@user.post("", status_code=201)
async def create_user(
    new_user: NewUserInput, api_key: str = Depends(is_admin)
) -> NewUserResponse:
    """Create a new entry in the database."""

    key, salt, hashed = generate_credentials()
    user = User(
        name=new_user.name,
        email=new_user.email,
        key=hashed,
        salt=salt,
        admin=new_user.admin,
    )
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError as err:
            raise HTTPException(
                status_code=400,
                detail="User already exists with the provided name & email.",
            )

    return NewUserResponse(
        name=user.name,
        email=user.email,
        key=key + ":" + salt,
    )


@user.get("")
async def get_user(email: str, api_key: str = Depends(is_admin)) -> UserResponse:
    """Get a user's information."""

    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).one_or_none()

        if not user:
            raise HTTPException(404, detail="User not found.")

        return UserResponse(**user.model_dump())


@user.patch("")
async def update_user(
    email: str, update: NewUserInput, api_key: str = Depends(is_admin)
) -> UserResponse:
    """Update a user's information."""

    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).one_or_none()

        if not user:
            raise HTTPException(404, detail="User not found.")

        email_exists = session.exec(
            select(User).where(User.email == update.email)
        ).one_or_none()

        if email_exists:
            raise HTTPException(400, detail="User already exists with provided email.")

        # apply the updates
        user.name = update.name
        user.email = update.email
        user.admin = update.admin

        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse(**user.model_dump())


@user.put("/rotate")
async def rotate_key(email: str, api_key: str = Depends(is_admin)) -> Message:
    """Rotate a user's key."""

    key, salt, hashed = generate_credentials()
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user.key = hashed
        user.salt = salt
        session.add(user)
        session.commit()
        session.refresh(user)

    return Message(
        detail=f"Key rotated for {user.name} ({user.email}); new key enclosed.",
        data=key + ":" + salt,
    )


@user.delete("")
async def delete_user(
    email: str, api_key: str = Depends(is_admin)
) -> Message:
    """Delete a user from the database."""

    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        name = user.name
        session.delete(user)
        session.commit()
        return Message(detail=f"User {name}, {email} deleted.")


@users.get("")
async def get_users(
    offset: int = 0, limit: int = 10, api_key: str = Depends(is_admin)
) -> list[UserResponse]:
    """Return the API's current users."""

    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be greater than 0.")

    if limit <= 0:
        raise HTTPException(
            status_code=400, detail="Limit must be greater than or equal to 1."
        )

    with Session(engine) as session:
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        users = [UserResponse(**user.model_dump()) for user in users]
        return users
