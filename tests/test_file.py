from unittest.mock import AsyncMock, patch

import pytest
from repository import SalesRepository
from service import fetch_sales_data_service, parse_sales_data_service
from tests.conftest import async_session_maker_new
from models import Sale, Product


@pytest.fixture
async def create_test_data():
    async with async_session_maker_new() as session:
        sale = Sale(date='2024-01-01')
        product1 = Product(name="Product A", quantity=10, price=5.0, category="Category 1", sale=sale)
        product2 = Product(name="Product B", quantity=20, price=10.0, category="Category 2", sale=sale)

        session.add(sale)
        session.add(product1)
        session.add(product2)
        await session.commit()

        yield sale

        await session.delete(sale)
        await session.commit()


async def test_get_total_revenue(create_test_data):
    sales_repository = SalesRepository(async_session_maker_new)
    date = create_test_data.date

    total_revenue = await sales_repository.get_total_revenue(date)

    expected_revenue = (10 * 5.0) + (20 * 10.0)
    assert total_revenue == expected_revenue


async def test_get_top_products(create_test_data):
    sales_repository = SalesRepository(async_session_maker_new)
    date = create_test_data.date

    top_products_names = await sales_repository.get_top_products(date)
    expected_top_products_names = 'Product B, Product A'

    assert top_products_names == expected_top_products_names


async def test_get_categories(create_test_data):
    sales_repository = SalesRepository(async_session_maker_new)
    date = create_test_data.date

    categories = await sales_repository.get_categories(date)
    expected_categories = 'Category 1: 10, Category 2: 20'

    assert categories == expected_categories


async def test_fetch_sales_data_success():
    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = 'Sales data'

        result = await fetch_sales_data_service()
        assert result == 'Sales data'

async def test_parse_sales_data_service():
    xml_content = """<sales date="2024-07-18">
                        <products>
                            <product>
                                <id>1</id>
                                <name>Товар 1</name>
                                <quantity>10</quantity>
                                <price>199.99</price>
                                <category>Категория 1</category>
                            </product>
                            <product>
                                <id>2</id>
                                <name>Товар 2</name>
                                <quantity>5</quantity>
                                <price>299.99</price>
                                <category>Категория 2</category>
                            </product>
                        </products>
                     </sales>"""

    expected_date = '2024-07-18'
    expected_products = [
        (1, 'Товар 1', 10, 199.99, 'Категория 1'),
        (2, 'Товар 2', 5, 299.99, 'Категория 2')
    ]

    sales_date, products = await parse_sales_data_service(xml_content)

    assert sales_date == expected_date
    assert products == expected_products