"""
THis router is for all users, site_owner or admin 
"""

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

router = APIRouter(tags=["Sites Routes"])
# cu, cs, cd, cqst, ccit, ccot = db.main()


@router.post("/site/registration", status_code=status.HTTP_201_CREATED)
async def signup(data: schemas.SiteRegistration, response: Response, token:str =  Depends(main.oauth2_scheme)):
    
    result = oauth.get_current_user(token=token)

    if isinstance(result , HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= ExceptionLiterals.INVALID_TOKEN,
        )
    try:
        admin_id = result.id
        user = dbquery.get_one_user(collection_user=main.ca, user_id=admin_id)
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= ExceptionLiterals.ID_NOT_FOUND,
            )

        # generate random password 5 
        # lUX3*T8!
        random_password = utils.generate_random_password(8)
        hashed_password = utils.hash(random_password)
        try:
            site_id = dbquery.register_site(
                collection_site=main.cs,
                admin_id=admin_id,
                email=data.email,
                password=hashed_password,
                name= data.name,
                location=data.location,
                total_capacity=data.totalCapacity,
                longitude=data.longitude,
                latitude=data.latitude,
            )

        except errors.DuplicateKeyError as ex:
            response.status_code = status.HTTP_409_CONFLICT
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= ExceptionLiterals.EMAIL_ALREADY_EXISTS + data.email,
            )

        return {
            "detail": SuccessLiterals.REGISTRATION_SUCCESSFUL,
            "siteId": site_id,
            "email": data.email,
            "password": random_password,
        }

    except Exception as ex:
        response.status_code = status.HTTP_409_CONFLICT
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.post("/site/login", status_code=status.HTTP_200_OK)
async def site_login(data: schemas.Login, response: Response):

    site = dbquery.site_login(main.cs, email=data.email)

    if not site:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
        )

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
    }
    

@router.get(
    "/site/profile", status_code=status.HTTP_200_OK, response_model=schemas.SiteProfile
)
async def site_profile(response: Response, token:str =  Depends(main.oauth2_scheme)):

    result = oauth.get_current_user(token=token)

    if isinstance(result , HTTPException):

        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= ExceptionLiterals.INVALID_TOKEN,
        )

    site_data: dict = dbquery.get_site(main.cs, site_id=result.id)
    profile_show_check = site_data.get("show_data")

    if not site_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= ExceptionLiterals.INVALID_TOKEN,
        )
    
    if not profile_show_check:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= ExceptionLiterals.ACCESS_REVOKED,
        )
    
    return site_data



# TODO: add _id in site profile as well