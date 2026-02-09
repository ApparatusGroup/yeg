from fastapi import APIRouter
from pydantic import BaseModel

from api.models.store import Store
from api.services.mock_catalog import list_stores as fetch_stores

router = APIRouter()


class StoresResponse(BaseModel):
    items: list[Store]
    total: int


@router.get('', response_model=StoresResponse)
async def list_stores() -> StoresResponse:
    items = fetch_stores()
    return StoresResponse(items=items, total=len(items))
