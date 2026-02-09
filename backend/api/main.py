from fastapi import FastAPI

from api.routers import products, search, stores
from config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(search.router, prefix='/search', tags=['search'])
app.include_router(products.router, prefix='/products', tags=['products'])
app.include_router(stores.router, prefix='/stores', tags=['stores'])


@app.get('/health')
async def healthcheck() -> dict[str, str]:
    return {'status': 'ok'}
