from sqlmodel import Field, SQLModel

from app.schemas.role import RoleBase


class Role(RoleBase, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)
