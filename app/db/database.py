from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel
from config.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
async def get_session():
    async with AsyncSession(engine) as session:
        yield session