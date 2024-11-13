from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from planner import planner
import pytz
my_timezone = pytz.timezone('Europe/Moscow')

@asynccontextmanager
async def planner_lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler(timezone=my_timezone)
    scheduler.add_job(func=planner, trigger='interval', days=1, start_date='2024-11-13 11:53:00')  # Исправлено
    scheduler.start()
    yield

app = FastAPI(lifespan=planner_lifespan)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
