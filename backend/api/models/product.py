from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl


class ProductBase(BaseModel):
    title: str
    description: str | None = None
    brand: str | None = None
    category: str | None = None
    price: Decimal | None = None
    currency: str = 'CAD'
    image_url: HttpUrl | None = None
    source_url: HttpUrl
    store_id: str
    neighborhood: str | None = None


class Product(ProductBase):
    id: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
