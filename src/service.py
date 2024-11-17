import asyncio
import logging
import os

import httpx
import datetime
import xml.etree.ElementTree as ET

from dotenv import load_dotenv

from logging_config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


load_dotenv()

api_key = os.getenv('CHAD_API_KEY')
CHAD_API_KEY =api_key


async def fetch_sales_data_service():
    log.info("Начало получения данных о продажах.")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('http://test_service:8001/sales-data')
            response.raise_for_status()
            log.info("Данные о продажах успешно получены.")
            return response.text
        except httpx.HTTPStatusError as e:
            log.error(f"Ошибка при получении данных о продажах: {e}")
            raise


async def parse_sales_data_service(xml_content):
    log.info("Начало разбора данных о продажах.")
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
        log.debug(
            f"Добавлен продукт: ID={product_id}, Название={name}, Количество={quantity}, Цена={price},"
            f" Категория={category}")

    log.info("Разбор данных о продажах завершен.")
    return sales_date, products


async def get_sales_service(sales_repository):
    log.info("Начинаем процесс получения и сохранения данных о продажах.")
    xml_content = await fetch_sales_data_service()
    sales_date, products = await parse_sales_data_service(xml_content)
    await sales_repository.add_sales(sales_date, products)
    log.info(f"Данные о продажах за {sales_date} успешно сохранены в репозитории.")


async def analyze_sales_service(sales_repository):
    log.info("Начинаем анализ данных о продажах.")
    async with httpx.AsyncClient() as client:
        date = datetime.date.today().isoformat()

        total_revenue = await sales_repository.get_total_revenue(date)
        top_products = await sales_repository.get_top_products(date)
        categories = await sales_repository.get_categories(date)

        prompt = (
            f'Проанализируй данные о продажах за {date}:\n'
            f'1. Общая выручка: {total_revenue}\n'
            f'2. Топ-3 товара по продажам: {top_products}\n'
            f'3. Распределение по категориям: {categories}\n\n'
            'Составь краткий аналитический отчет с выводами и рекомендациями.'
        )

        request_json = {
            "message": prompt,
            "api_key": CHAD_API_KEY
        }

        max_retries = 3
        attempts = 0
        answer = ""

        while attempts < max_retries:
            try:
                response = await client.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini', json=request_json)
                if response.is_success:
                    answer = response.json().get("response", "")
                    log.info("Анализ данных о продажах успешно завершен.")
                    break
                else:
                    attempts += 1
                    log.error(
                        f"Ошибка при получении ответа от API для анализа данных. Код статуса: {response.status_code}. "
                        f"Попытка {attempts}/{max_retries}.")
            except Exception as e:
                attempts += 1
                log.error(f"Произошла ошибка при обращении к API: {e}. Попытка {attempts}/{max_retries}.")

            await asyncio.sleep(5)

        if attempts == max_retries:
            answer = "Не удалось получить ответ от API."
            log.error("Все попытки обращения к API исчерпаны. Проверьте работоспособность сервиса.")

        await sales_repository.add_analysis(date, answer)
        log.info(f"Анализ за дату {date} успешно сохранён.")