from datetime import datetime

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    name: str
    last_name: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(SQLModel):
    username: str
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    last_name: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
