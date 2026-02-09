from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from api.models.product import Product
from api.models.store import Store

NOW = datetime.now(UTC)

_MOCK_STORES: list[Store] = [
    Store(
        id='store-1',
        name='River Valley Goods',
        domain='rivervalleygoods.example',
        homepage_url='https://rivervalleygoods.example',
        platform='shopify',
        neighborhood='Strathcona',
        opted_out=False,
    )
]

_MOCK_PRODUCTS: list[Product] = [
    Product(
        id='prod-1',
        title='Small Batch Honey',
        description='Raw Alberta wildflower honey from a local producer.',
        brand='River Valley Goods',
        category='Groceries',
        price=Decimal('14.99'),
        currency='CAD',
        image_url='https://images.example.com/products/honey.jpg',
        source_url='https://rivervalleygoods.example/products/small-batch-honey',
        store_id='store-1',
        neighborhood='Strathcona',
        is_active=True,
        created_at=NOW,
        updated_at=NOW,
    )
]


def list_products() -> list[Product]:
    return _MOCK_PRODUCTS


def get_product(product_id: str) -> Product | None:
    return next((product for product in _MOCK_PRODUCTS if product.id == product_id), None)


def list_stores() -> list[Store]:
    return _MOCK_STORES
