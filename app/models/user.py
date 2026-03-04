from pydantic import BaseModel


class UserLogIn(BaseModel):
    username:str
    password:str
    
class UserRegister(BaseModel):
    firstName:str
    lastName:str
    church:str
    phoneNumber:str
    email:str
    username:str
    password:str
    role:str

class UserPublic(BaseModel):
    id:str
    firstName:str
    lastName:str
    church:str
    phoneNumber:str
    email:str
    username:str
    role:str