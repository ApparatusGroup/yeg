from crawler.extractors.base import BaseExtractor


class SquareExtractor(BaseExtractor):
    async def extract(self, store_url: str) -> list[dict]:
        return []
