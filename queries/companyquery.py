from src.database import async_engine, Base
from src.database import async_session_factory as asf
from src.models import CompaniesOrm

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_company():
        async with asf() as session:
            new_worker = CompaniesOrm(name="1")
            session.add(new_worker)
            await session.commit()