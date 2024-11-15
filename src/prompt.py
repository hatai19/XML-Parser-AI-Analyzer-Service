import logging

import httpx
import datetime

from repository import total_revenue_repository, top_products_repository, categories_repository, \
    save_analysis_repository

logging.basicConfig(level=logging.INFO)


async def analyze_sales():
    async with httpx.AsyncClient() as client:
        date = datetime.date.today().isoformat()
        total_revenue = await total_revenue_repository(date)
        top_products = await top_products_repository(date)
        categories = await categories_repository(date)
        CHAD_API_KEY = 'chad-fa58b83336154947a990a49d3925fdd1lqdur28n'

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

        response = await client.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini',
                                 json=request_json)

        if response.is_success:
            answer = response.json().get("response", "")
        else:
            answer = "Не удалось получить ответ от API."

        await save_analysis_repository(date, answer)