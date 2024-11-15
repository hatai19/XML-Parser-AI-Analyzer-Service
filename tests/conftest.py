import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# from src.auth.service import get_current_user
# from src.database import get_db
# from src.main import app
# from src.auth.models import Base
#
# metadata = Base.metadata
#
# DATABASE_URL_TEST = f"postgresql+asyncpg://postgres:7712@localhost:5434/postgres"
#
# engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
# async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
# metadata.bind = engine_test
#
# async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
# app.dependency_overrides[get_db] = override_get_async_session
#
# @pytest.fixture(autouse=True, scope='session')
# async def prepare_database():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#     yield
#     async with engine_test.begin() as conn:
#         await conn.run_sync(metadata.drop_all)

# SETUP
# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="session")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac
