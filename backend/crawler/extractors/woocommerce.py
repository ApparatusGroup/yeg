from crawler.extractors.base import BaseExtractor


class WooCommerceExtractor(BaseExtractor):
    async def extract(self, store_url: str) -> list[dict]:
        return []
