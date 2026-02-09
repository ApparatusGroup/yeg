import httpx

from crawler.extractors.base import BaseExtractor


class ShopifyExtractor(BaseExtractor):
    async def extract(self, store_url: str) -> list[dict]:
        endpoint = store_url.rstrip('/') + '/products.json?limit=250'
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
        payload = response.json()
        return payload.get('products', [])
