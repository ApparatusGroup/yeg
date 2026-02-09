from fastapi import APIRouter

router = APIRouter()


@router.get('')
async def list_stores() -> dict:
    return {'items': [], 'total': 0}
