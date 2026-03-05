from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from utils.utils import create_access_token, create_refresh_token, hash_password, verify_password
from db.database import get_session
from models.user import User, UserLogIn, UserPublic, UserRegister
from models.token import Token
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
async def register(user_in:UserRegister, session:AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user_in.username))
    
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pass = hash_password(user_in.password)
    
    new_user = User(
        firstName=user_in.first_name,
        lastName=user_in.last_name,
        church=user_in.church,
        phoneNumber=user_in.phone_number,
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_pass
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    public_user = UserPublic.model_validate(new_user)
    return public_user

@router.post("/login", response_model=Token)
async def login(user_in:OAuth2PasswordRequestForm= Depends(), session:AsyncSession = Depends(get_session)):
    username = user_in.username
    password = user_in.password
    
    results = await session.execute(select(User).where(User.username ==username))
    user:User = results.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate":"Bearer"})
    
    access_token = create_access_token(user_in.username)
    refresh_token = create_refresh_token(user_in.username)
    
    
    
    