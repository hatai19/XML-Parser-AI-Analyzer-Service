from fastapi import FastAPI
from fastapi.responses import Response
from xml.etree.ElementTree import Element, SubElement, tostring
import datetime

from fastapi.routing import APIRouter

test_router = APIRouter()


@test_router.get("/sales-data", response_class=Response)
async def get_sales_data():
    sales_data = Element('sales_data', date=datetime.date.today().strftime("%Y-%m-%d"))

    products = SubElement(sales_data, 'products')

    product1 = SubElement(products, 'product')
    SubElement(product1, 'id').text = '1'
    SubElement(product1, 'name').text = 'Product A'
    SubElement(product1, 'quantity').text = '100'
    SubElement(product1, 'price').text = '1500.00'
    SubElement(product1, 'category').text = 'Electronics'

    product2 = SubElement(products, 'product')
    SubElement(product2, 'id').text = '2'
    SubElement(product2, 'name').text = 'Product B'
    SubElement(product2, 'quantity').text = '200'
    SubElement(product2, 'price').text = '800.00'
    SubElement(product2, 'category').text = 'Home Appliances'

    product3 = SubElement(products, 'product')
    SubElement(product3, 'id').text = '3'
    SubElement(product3, 'name').text = 'Product C'
    SubElement(product3, 'quantity').text = '150'
    SubElement(product3, 'price').text = '1200.00'
    SubElement(product3, 'category').text = 'Furniture'

    product4 = SubElement(products, 'product')
    SubElement(product4, 'id').text = '4'
    SubElement(product4, 'name').text = 'Product D'
    SubElement(product4, 'quantity').text = '250'
    SubElement(product4, 'price').text = '300.00'
    SubElement(product4, 'category').text = 'Toys'

    xml_bytes = tostring(sales_data, encoding='utf-8', method='xml')

    return Response(content=xml_bytes, media_type='application/xml')