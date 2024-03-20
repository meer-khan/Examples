from fastapi import status, APIRouter, Response
from icecream import ic

router = APIRouter(tags=["profile"])

@router.post("/profile", status_code=status.HTTP_200_OK)
async def profile():
   return {"msg": "profile route is working fine"}