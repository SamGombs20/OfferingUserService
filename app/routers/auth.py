from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from utils.utils import hash_password
from db.database import get_session
from models.user import User, UserPublic, UserRegister
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
    return new_user

    
    