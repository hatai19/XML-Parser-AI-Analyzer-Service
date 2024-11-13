from src.database import Session
from src.models import Sale, Product
import logging

logging.basicConfig(filename='celery.log', level=logging.ERROR)

def store_sales_data_repository(sales_date, products):
    session = Session()
    try:
        new_sale = Sale(date=sales_date)
        session.add(new_sale)
        session.commit()
        sale_id = new_sale.id

        for product_id, name, quantity, price in products:
            new_product = Product(id=product_id, name=name, quantity=quantity, price=price, sale_id=sale_id)
            session.add(new_product)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()