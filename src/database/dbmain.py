from sqlmodel import create_engine,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config
from config import Config
from database.models import Gym
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine=AsyncEngine(create_engine(url=Config.DATABASE_URL,echo=True)) # echo used to see the all sql that will be logged on every transaction

async def init_db():
    async with async_engine.begin() as conn: #transactional context to interact with the database
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()->AsyncSession: # session dependency injection
    Session=sessionmaker(bind=async_engine,class_=AsyncSession, expire_on_commit=False) #Creates a new session factory bound to the database engine
    async with Session() as session:
        yield session