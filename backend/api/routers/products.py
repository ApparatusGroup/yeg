from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.models.product import Product
from api.services.mock_catalog import get_product, list_products as fetch_products

router = APIRouter()


class ProductsResponse(BaseModel):
    items: list[Product]
    total: int


@router.get('', response_model=ProductsResponse)
async def list_products() -> ProductsResponse:
    items = fetch_products()
    return ProductsResponse(items=items, total=len(items))


@router.get('/{product_id}', response_model=Product)
async def get_product_by_id(product_id: str) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product
