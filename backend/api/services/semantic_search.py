from api.models.search import SearchRequest, SearchResponse


async def run_semantic_search(payload: SearchRequest) -> SearchResponse:
    """Placeholder semantic search service. Returns empty results until DB/vector integration is added."""
    return SearchResponse(query=payload.query, total=0, products=[])
