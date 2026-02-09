from pydantic import BaseModel

from api.models.product import Product


class SearchRequest(BaseModel):
    query: str
    neighborhood: list[str] | None = None
    vibes: list[str] | None = None
    page: int = 1
    page_size: int = 24


class SearchResponse(BaseModel):
    query: str
    total: int
    products: list[Product]
