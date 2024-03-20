from fastapi import status, APIRouter, Response, HTTPException
from icecream import ic


router = APIRouter(tags=["login"])

@router.post("/login", status_code=status.HTTP_200_OK)
async def login():
   return {"msg": "everything working fine",}