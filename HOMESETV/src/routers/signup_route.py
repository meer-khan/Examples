from fastapi import status, APIRouter, Response, HTTPException, Form
from icecream import ic
from pydantic import ValidationError
from pymongo import errors
import datetime
from schemas import schemas
import app
from db import db_query
import sys

from utils import password_manager

router = APIRouter(tags=["user-management"], prefix="/user")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    response: Response,
    userName: str = Form(...),
    email: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(...),
    termsConditions: bool = Form(...),
):
    try:
        user_data = {
            "userName": userName,
            "email": email,
            "password1": password1,
            "password2": password2,
            "termsConditions": termsConditions,
        }
        ic(user_data)
        try:
            user_data = schemas.Signup(
                userName=userName,
                email=email,
                password1=password1,
                password2=password2,
                termsConditions=termsConditions,
                
            )
        except ValidationError as exc_info:
            ic(exc_info)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=exc_info.errors()
            )

        user_data = user_data.model_dump()
        user_data["password"] = password_manager.hash(user_data["password1"])
        user_data.pop("password1")
        user_data.pop("password2")
        user_data.update(
            {
                "roles": ["user"],
                "plan": None,
                "createdAt": datetime.datetime.now(datetime.UTC),
                "updatedAt": datetime.datetime.now(datetime.UTC),
                "active": True,
                "passVer": 1
            }
        )
        inserted_record = db_query.insert_records(
            collection=app.col_user, data=user_data
        )
        # TODO: Log - I
        return {"detail": "user registered successfully"}

    except errors.DuplicateKeyError as ex:
        # TODO: Log - W {ex}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists with this email",
        )

    except Exception as ex:
        # TODO: Log - C
        ic(ex)
        ic(type(ex))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error",
        )
