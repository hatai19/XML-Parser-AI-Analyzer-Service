from sqlalchemy import select, func, asc

from models import Product, Sale, Analysis

class SalesRepository:
    def __init__(self, async_sessionmaker):
        self.async_sessionmaker = async_sessionmaker

    async def add_sales(self, sales_date, products):
        async with self.async_sessionmaker() as session:
            try:
                new_sale = Sale(date=sales_date)
                session.add(new_sale)

                await session.flush()
                sale_id = new_sale.id

                for product_id, name, quantity, price, category in products:
                    new_product = Product(
                        id=product_id,
                        name=name,
                        category=category,
                        quantity=quantity,
                        price=price,
                        sale_id=sale_id
                    )
                    session.add(new_product)

                await session.commit()

            except Exception as e:
                await session.rollback()
                raise e

    async def get_total_revenue(self, date):
        async with self.async_sessionmaker() as session:
            total_revenue_result = await session.execute(
                select(func.sum(Product.price * Product.quantity))
                .join(Sale)
                .filter(Sale.date == date)
            )

            total_revenue = total_revenue_result.scalar() or 0
            return total_revenue

    async def get_top_products(self, date):
        async with self.async_sessionmaker() as session:
            top_products_result = await session.execute(
                select(Product.name, func.sum(Product.quantity))
                .join(Sale)
                .filter(Sale.date == date)
                .group_by(Product.name)
                .order_by(func.sum(Product.quantity).desc())
                .limit(3)
            )
            top_products = top_products_result.fetchall()
            top_products_names = [name for name, _ in top_products]
            return ', '.join(top_products_names)

    async def get_categories(self, date):
        async with self.async_sessionmaker() as session:
            categories_result = await session.execute(
                select(Product.category, func.sum(Product.quantity))
                .join(Sale)
                .filter(Sale.date == date)
                .group_by(Product.category)
                .order_by(asc(Product.category))
            )
            categories = categories_result.all()
            categories_string = ', '.join([f'{category}: {quantity}' for category, quantity in categories])
            return categories_string

    async def add_analysis(self, date, answer):
        async with self.async_sessionmaker() as session:
            async with session.begin():
                analysis = Analysis(date=date, answer=answer)
                session.add(analysis)

                await session.commit()

