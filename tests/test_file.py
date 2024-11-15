import pytest
from sqlalchemy.orm import defer

from async_database import async_session
from repository import total_revenue_repository, top_products_repository, categories_repository


@pytest.mark.asyncio
async def test_total_revenue_repository():
    total_revenue = await total_revenue_repository('2024-11-14')

    assert total_revenue == 565000.0


@pytest.mark.asyncio
async def test_top_products_repository():
    top_products_names = await top_products_repository('2024-11-14')
    expected_top_products_names = 'Product D, Product B, Product C'

    assert top_products_names == expected_top_products_names

@pytest.mark.asyncio
async def test_categories_repository():
    categories = await categories_repository('2024-11-14')
    expected_categories = "Electronics: 100, Furniture: 150, Home Appliances: 200, Toys: 250"
    assert categories == expected_categories
