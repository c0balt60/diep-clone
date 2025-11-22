from fastapi import APIRouter

router = APIRouter()

@router.get("/score")
async def score():
    return {"score": 50}
