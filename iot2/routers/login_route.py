
from fastapi import status, HTTPException, Depends, APIRouter, Response
from pymongo import errors
from typing import List
from icecream import ic
from message_literals.messages import ExceptionLiterals, SuccessLiterals
import dbquery
import oauth
import schemas
import utils
import main

router = APIRouter(tags=["Login Route"])

@router.post("/login", status_code=status.HTTP_200_OK)
async def site_login(data: schemas.Login, response: Response):
    try:
        site = dbquery.site_login(main.cs, email=data.email)
        admin = dbquery.admin_login(main.ca, email=data.email)

        if site:
            hashed_password = site.get("password")
            result = utils.verify(data.password, hashed_password)
            if not result:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
                )

            access_token = oauth.create_access_token(
                {"email": site.get("email"), "id": str(site.get("_id"))}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "role": "manager"
            }
        
        elif admin:
            hashed_password = admin.get("password")
            pass_verify = utils.verify(data.password, hashed_password)

            if not pass_verify:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
                )

            access_token = oauth.create_access_token(
                {"email": admin.get("email"), "id": str(admin.get("_id"))}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "role": "admin"
            }
        
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
            )
        
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )
    