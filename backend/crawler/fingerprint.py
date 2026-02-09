from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup


@dataclass(slots=True)
class FingerprintResult:
    url: str
    platform: str
    confidence: float
    reason: str


def detect_platform(html: str, headers: httpx.Headers) -> tuple[str, float, str]:
    text = html.lower()
    soup = BeautifulSoup(html, 'html.parser')

    if 'x-shopify-stage' in headers or 'x-shopid' in headers or 'cdn.shopify.com' in text:
        return 'shopify', 0.95, 'shopify headers/assets detected'

    if '/wp-content/plugins/woocommerce' in text or '/wc-api/' in text:
        return 'woocommerce', 0.9, 'woocommerce assets detected'

    if 'squareup.com' in text or 'sq-payment-form' in text:
        return 'square', 0.85, 'square commerce markers found'

    if soup.find('script', string=lambda s: s and 'Shopify' in s):
        return 'shopify', 0.8, 'shopify script marker found'

    return 'unknown', 0.1, 'no known markers found'


async def fingerprint_url(url: str, timeout: float = 15.0) -> FingerprintResult:
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; yeg-shadow/1.0)'}
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        response = await client.get(url, headers=headers)

    platform, confidence, reason = detect_platform(response.text, response.headers)
    return FingerprintResult(url=url, platform=platform, confidence=confidence, reason=reason)
