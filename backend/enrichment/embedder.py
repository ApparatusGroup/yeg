from api.services.embedding import embed_text


async def embed_product_text(product_text: str) -> list[float]:
    return await embed_text(product_text)
