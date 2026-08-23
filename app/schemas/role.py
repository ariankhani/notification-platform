from datetime import datetime

from sqlmodel import Field, SQLModel


class RoleBase(SQLModel):
    name:str = Field(index=True, unique=True)
    description: str | None = None


class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    

class UserRoleAssign(SQLModel): 
    user_id: int
    role_id: int
    
