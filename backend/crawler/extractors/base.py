from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    @abstractmethod
    async def extract(self, store_url: str) -> list[dict]:
        raise NotImplementedError
