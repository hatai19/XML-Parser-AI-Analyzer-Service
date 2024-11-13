import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

database_url = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

# async_engine = create_async_engine('postgresql+asyncpg://postgres:postgres@products_db:5432/postgres')
# async_session = async_sessionmaker(async_engine)
#
#
# async def get_db() -> AsyncSession:
#     async with async_session() as session:
#         yield session



engine = create_engine(database_url)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Dependency to get a session, similar to how you would use in a FastAPI app
# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()