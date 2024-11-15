import xml.etree.ElementTree as ET

from unicodedata import category

from models import Sale, Product
import requests
from database import Session


def fetch_sales_data():
    try:
        response = requests.get('http://second:8001/sales-data')
        response.raise_for_status()
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
        category = product_elem.find('category').text
        quantity = int(product_elem.find('quantity').text)
        price = float(product_elem.find('price').text)
        products.append((product_id, name, category, quantity, price))

    return sales_date, products


def add_sales_to_db(sales_date, products):
    session = Session()
    try:
        new_sale = Sale(date=sales_date)
        session.add(new_sale)

        session.commit()

        sale_id = new_sale.id

        for product_id, name, quantity, price in products:
            new_product = Product(id=product_id, name=name, category=category,
                                  quantity=quantity, price=price, sale_id=sale_id)
            session.add(new_product)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def planner():
    try:
        xml_content = fetch_sales_data()
        sales_date, products = parse_sales_data(xml_content)
        add_sales_to_db(sales_date, products)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

