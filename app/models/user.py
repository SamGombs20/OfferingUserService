from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    first_name:str = Field(..., alias="firstName")
    last_name:str = Field(..., alias="lastName")
    church:str
    phone_number:str = Field(..., alias="phoneNumber")
    email:EmailStr
    username:str
    role:str = "user"
    class Config:
        populate_by_name = True
        from_attributes = True

class User(UserBase, table=True):
    __tablename__ = "analysis_users"
    id:UUID = Field(default_factory=uuid4, 
                    primary_key=True)
    hashed_password:str
    created_at:datetime = Field(default_factory=datetime.utcnow)

class UserLogIn(SQLModel):
    username:str
    password:str
    
class UserRegister(UserBase):
    password:str

class UserPublic(UserBase):
    id:UUID
    role:str