import httpx
import xml.etree.ElementTree as ET


# from database import get_db
from models import Sale, Product

# async def fetch_sales_data():
#     async with httpx.AsyncClient() as client:
#         response = await client.get('http://localhost:8000/sales-data')
#         response.raise_for_status()
#         return response.text

import requests
from database import Session


def fetch_sales_data():
    try:
        response = requests.get('http://second:8001/sales-data')
        response.raise_for_status()  # This will raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def parse_sales_data(xml_content):
    root = ET.fromstring(xml_content)
    sales_date = root.attrib.get('date')
    products = []

    for product_elem in root.find('products'):
        product_id = int(product_elem.find('id').text)
        name = product_elem.find('name').text
        quantity = int(product_elem.find('quantity').text)
        price = float(product_elem.find('price').text)
        products.append((product_id, name, quantity, price))

    return sales_date, products


def add_sales_to_db(sales_date, products):
    session = Session()
    try:
        # Создаем новый объект Sale и добавляем его в сессию
        new_sale = Sale(date=sales_date)
        session.add(new_sale)

        # Коммитим сессию, чтобы ID для нового объекта Sale был установлен
        session.commit()

        sale_id = new_sale.id  # Получаем ID только что добавленного объекта Sale

        # Добавляем продукты, связанные с этой продажей
        for product_id, name, quantity, price in products:
            new_product = Product(id=product_id, name=name, quantity=quantity, price=price, sale_id=sale_id)
            session.add(new_product)

        # Совершаем второй коммит после добавления всех продуктов
        session.commit()
    except Exception as e:
        session.rollback()  # Откат изменений при ошибке
        raise e  # Повторно выбрасываем исключение, чтобы оно могло быть обработано выше
    finally:
        session.close()

def planner():
    try:
        xml_content = fetch_sales_data()
        sales_date, products = parse_sales_data(xml_content)
        add_sales_to_db(sales_date, products)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

