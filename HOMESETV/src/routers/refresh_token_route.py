from fastapi import status, APIRouter, Response, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from bson import ObjectId
from db import db_query
from utils import oauth, password_manager
from schemas import schemas
from icecream import ic
import app


router = APIRouter(tags=["user-management"], prefix="/user")


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(response: Response, refreshToken:dict = Depends(oauth.get_refresh_token)):
    try:
        ic(refreshToken)
        # id = oauth.verify_refresh_token(refreshToken)
        payload:dict = refreshToken
        query_dict = {"_id": ObjectId(payload.get("sub")), "passVer": payload.get("ver")}
        user: dict = db_query.find_single_record(app.col_user, query_dict)
        ic(user)
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )

        else:
            access_token = oauth.create_access_token(
                {"sub": str(user.get("_id")), "ver": user.get("passVer")}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "role": user.get("role"),
            }

    except Exception as ex:
        # TODO: LOG - C {ex}
        ic(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error",
        )
