from uuid import UUID

from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    first_name:str = Field(..., alias="firstName")
    last_name:str = Field(..., alias="lastName")
    church:str
    phone_number:str = Field(..., alias="phoneNumber")
    email:EmailStr
    username:str
    
    class Config:
        populate_by_name = True
        from_attributes = True

class User(UserBase, table=True):
    __tablename__ = "analysis_users"
    id:UUID = Field(default=None, primary_key=True)
    hashed_password:str

class UserLogIn(SQLModel):
    username:str
    password:str
    
class UserRegister(UserBase):
    password:str

class UserPublic(UserBase):
    id:UUID
    role:str