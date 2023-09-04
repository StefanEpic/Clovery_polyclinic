import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from models.polyclinic import *
from db.db import get_session
from schemas.polyclinic import SpecializationCreate, QualificationCreate, PolyclinicCreate, PatientCreate

DATABASE_URL_TEST = 'sqlite+aiosqlite:///test.db'

engine_test = create_async_engine(DATABASE_URL_TEST)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            specialization = SpecializationCreate(title='Педиатр')
            qualification = QualificationCreate(title='Лаборант')
            polyclinic = PolyclinicCreate(title='Главная Детская №5', address='ул. Главная, д. 5')
            patient = PatientCreate(first_name='Иван',
                                    second_name='Иванов',
                                    last_name='Иванович',
                                    phone='+77777777777',
                                    email='ivan@test.com',
                                    address='ул. Пушкин, д. 10',
                                    polyclinic_id=1)

            session.add(Specialization(**specialization.model_dump()))
            session.add(Qualification(**qualification.model_dump()))
            session.add(Polyclinic(**polyclinic.model_dump()))
            session.add(Patient(**patient.model_dump()))
            await session.commit()

        yield

        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
