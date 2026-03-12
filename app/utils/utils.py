from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi import  HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from models.token import TokenPayload
from config.config import settings
from jose import JWSError, JWTError, jwt

from passlib.context import CryptContext

context = CryptContext(schemes=["argon2"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def hash_password(password:str)->str:
    return context.hash(password)

def verify_password(plain_pass:str, hash_pass:str)->bool:
    return context.verify(plain_pass, hash_pass)

def create_access_token(username:str)->str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    
    to_encode ={
        "sub":username,
        "exp":expire,
        "iat":datetime.utcnow()
    }
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
def create_refresh_token(username:str)->str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_IN_DAYS)
    
    to_encode = {
        "sub":username,
        "exp":expire,
        "iat":datetime.utcnow(),
        "token_type":"refresh"
    }
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
def decode_token(token:str)->Optional[Dict[str, any]]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except (JWTError, JWSError):
        return None
    
def get_current_user(token:str=Depends(oauth2_scheme))->str:
    try:
        print(token)
        payload:Dict[str, any] = decode_token(token)
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) <datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate":"Bearer"}
            )
        return token_data.sub
    except (JWTError, ValidationError):
        raise JWTError()