import logging

import httpx
import xml.etree.ElementTree as ET


from async_database import  async_session
from models import Sale, Product
from prompt import analyze_sales

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)


async def async_fetch_sales_data():
    logger.info("Fetching sales data from the external service.")
    async with httpx.AsyncClient() as client:
        response = await client.get('http://second:8001/sales-data')
        response.raise_for_status()
        logger.info("Sales data fetched successfully.")
        return response.text


async def async_parse_sales_data(xml_content):
    logger.info("Parsing sales data from XML content.")
    root = ET.fromstring(xml_content)
    sales_date = root.attrib.get('date')
    products = []

    for product_elem in root.find('products'):
        product_id = int(product_elem.find('id').text)
        name = product_elem.find('name').text
        quantity = int(product_elem.find('quantity').text)
        price = float(product_elem.find('price').text)
        category = product_elem.find('category').text
        products.append((product_id, name, quantity, price, category))

    logger.info(f"Parsed {len(products)} products from sales data.")
    return sales_date, products


async def async_add_sales_to_db(sales_date, products):
    async with async_session() as session:
        async with session.begin():
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


async def async_planner():
    try:
        logger.info("Starting sales data planner.")
        xml_content = await async_fetch_sales_data()
        sales_date, products = await async_parse_sales_data(xml_content)
        await async_add_sales_to_db(sales_date, products)
        logger.info("Sales data processing completed successfully.")
        await analyze_sales()
    except Exception as e:
        logger.error(f"An error occurred in the planner: {e}")