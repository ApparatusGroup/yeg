from fastapi import APIRouter

from api.models.search import SearchRequest, SearchResponse
from api.services.semantic_search import run_semantic_search

router = APIRouter()


@router.post('', response_model=SearchResponse)
async def search(payload: SearchRequest) -> SearchResponse:
    return await run_semantic_search(payload)
