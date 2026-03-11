
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlmodel import select

from db.database import get_session
from utils.utils import get_current_user
from models.user import User, UserPublic
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter(prefix="/users")
@router.get("/me", response_model=UserPublic)
async def read_user(current_user:str = Depends(get_current_user), session:AsyncSession=Depends(get_session)):
    result = await session.execute(select(User).where(User.username==current_user))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return user