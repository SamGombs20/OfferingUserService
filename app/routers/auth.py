from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from db.database import get_session
from models.user import User, UserPublic, UserRegister
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
async def register(user_in:UserRegister, session:AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user_in.username))
    
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")
    