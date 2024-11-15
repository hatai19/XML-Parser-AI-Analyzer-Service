from sqlalchemy import select, func, asc

from async_database import async_session
from models import Product, Sale, Analysis


async def total_revenue_repository(date):
    async with async_session() as session:
        async with session.begin():
            total_revenue_result = await session.execute(
                select(func.sum(Product.price*Product.quantity))
                .join(Sale)
                .filter(Sale.date == date)
            )

            total_revenue = total_revenue_result.scalar() or 0

    return total_revenue

async def top_products_repository(date):
    async with async_session() as session:
        async with session.begin():
            top_products_result = await session.execute(
                select(Product.name, func.sum(Product.quantity)).join(Sale)
                .filter(Sale.date == date)
                .group_by(Product.name)
                .order_by(func.sum(Product.quantity).desc())
                .limit(3)
            )
            top_products = top_products_result.fetchall()
            top_products_names = [name for name, _ in top_products]
            return ', '.join(top_products_names)

async def categories_repository(date):
    async with async_session() as session:
        async with session.begin():
            categories_result = await session.execute(
                select(Product.category, func.sum(Product.quantity)).join(Sale).filter(Sale.date == date)
                .group_by(Product.category).order_by(asc(Product.category))
            )
            categories = categories_result.all()
            categories_string = ', '.join([f'{category}: {quantity}' for category, quantity in categories])
            return categories_string


async def save_analysis_repository(date, answer):
    async with async_session() as session:
        async with session.begin():
            analysis = Analysis(date=date, answer=answer)
            session.add(analysis)

            await session.commit()