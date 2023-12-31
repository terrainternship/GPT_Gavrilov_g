import asyncio
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from create_bot import POSTGRE_HOST, POSTGRE_PORT, POSTGRE_DB, POSTGRE_USER, POSTGRE_PASSW
from config import RECREATE_DB
from logger.logger import logger
from dbase.models import Base


db_url = f'postgresql+asyncpg://{POSTGRE_USER}:{POSTGRE_PASSW}@{POSTGRE_HOST}/{POSTGRE_DB}'

def init_db() -> None:
    logger.info(f'Platform: {sys.platform}')
    logger.info(f'init_db:\n - {POSTGRE_HOST =}\n - {POSTGRE_PORT =}\n - {POSTGRE_DB =}\n - {POSTGRE_USER =}')
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def get_async_engine() -> create_async_engine:
    return create_async_engine(db_url, echo=True)

async def get_async_session(engine: create_async_engine) -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session()

async def connect_db() -> AsyncSession:
    engine = await get_async_engine()
    return await get_async_session(engine)

async def create_db() -> None:
    engine = await get_async_engine()
    async with engine.begin() as conn:
        if RECREATE_DB:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    init_db()
    asyncio.run(create_db())