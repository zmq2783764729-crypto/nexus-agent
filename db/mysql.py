from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from collections.abc import AsyncGenerator

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,#输出执行的sql语句 和debug一致
    pool_pre_ping=True,
    pool_size = 10,#连接数
    max_overflow=20,#溢出数量 自动销毁大于此值的连接
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session