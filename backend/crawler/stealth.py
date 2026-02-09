import asyncio
from urllib.parse import urlparse


class DomainRateLimiter:
    def __init__(self, delay_seconds: float = 2.0) -> None:
        self.delay_seconds = delay_seconds
        self._locks: dict[str, asyncio.Lock] = {}

    async def wait_turn(self, url: str) -> None:
        domain = urlparse(url).netloc
        lock = self._locks.setdefault(domain, asyncio.Lock())
        async with lock:
            await asyncio.sleep(self.delay_seconds)
