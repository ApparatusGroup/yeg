from fastapi import APIRouter

router = APIRouter()


@router.get('')
async def list_products() -> dict:
    return {'items': [], 'total': 0}
