import asyncio
import os
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from main import app
from models import Base

metadata = Base.metadata

load_dotenv()

db_user = os.getenv('DB_TEST_USER')
db_pass = os.getenv('DB_TEST_PASS')
db_host = os.getenv('DB_TEST_HOST')
db_port = os.getenv('DB_TEST_PORT')
db_name = os.getenv('DB_TEST_NAME')

database_url = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

engine_test = create_async_engine(database_url)
async_session_maker_new = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test



@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
