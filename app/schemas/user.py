"""Pydantic model for a new user."""

from pydantic import BaseModel, EmailStr, Field


class NewUserInput(BaseModel):
    name: str
    email: EmailStr
    admin: int = Field(default=0, ge=0, le=1)


class NewUserResponse(BaseModel):
    name: str
    email: EmailStr
    key: str


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    admin: int
