async def enrich_product_payload(raw_text: str) -> dict:
    """Stub for LLM enrichment logic (neighborhood + vibe tagging)."""
    return {
        'clean_description': raw_text.strip(),
        'vibes': [],
        'confidence': 0.0,
    }
