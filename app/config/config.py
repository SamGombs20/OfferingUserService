import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

class Settings(BaseSettings):
    SECRET_KEY:str = SECRET_KEY
    ACCESS_TOKEN_EXPIRE_IN_MINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_IN_DAYS:int=7
    ALGORITHM:str = "HS256"
    
settings = Settings()
    