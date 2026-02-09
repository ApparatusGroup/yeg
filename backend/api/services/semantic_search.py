from api.models.search import SearchRequest, SearchResponse
from api.services.mock_catalog import list_products


async def run_semantic_search(payload: SearchRequest) -> SearchResponse:
    """Temporary search implementation backed by mock catalog data."""
    products = list_products()
    query = payload.query.strip().lower()
    if query:
        products = [
            product
            for product in products
            if query in product.title.lower()
            or (product.description and query in product.description.lower())
        ]

    return SearchResponse(query=payload.query, total=len(products), products=products)
