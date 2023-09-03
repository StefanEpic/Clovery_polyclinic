from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

DATABASE_URL = 'sqlite+aiosqlite:///sqlite.db'
engine = create_async_engine(DATABASE_URL)


async def get_session() -> AsyncSession:
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
