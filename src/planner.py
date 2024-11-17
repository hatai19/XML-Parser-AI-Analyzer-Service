from database import async_session_maker
from service import get_sales_service, analyze_sales_service
from repository import SalesRepository


async def async_planner():
    sales_repository = SalesRepository(async_session_maker)
    await get_sales_service(sales_repository)
    await analyze_sales_service(sales_repository)
