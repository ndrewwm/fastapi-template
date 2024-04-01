"""User table."""

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User table, holding attributes (e.g. user's API key)."""

    email: str = Field(primary_key=True)
    name: str = Field()
    key: str = Field()
    salt: str = Field()
    admin: int = Field(ge=0, le=1)
