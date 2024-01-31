"""
THis router is for all users, site_owner or admin 
"""

from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pymongo import errors
from icecream import ic
import dbquery
import oauth
import schemas
import utils
import main 

router = APIRouter(tags=["User Routes"])
# cu, cs, cd, cqst, ccit, ccot = db.main()


@router.post("/site-registration", status_code=status.HTTP_201_CREATED)
async def signup(data: schemas.SiteRegistration, response: Response):
    try:
        admin_id = data.adminId
        user = dbquery.get_one_user(collection_user=main.cu, user_id=admin_id)
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Admin with id {admin_id} does not exists",
            )

        # generate random password
        # WO_z!NOn
        # [,NDgdDa
        random_password = utils.generate_random_password(8)
        hashed_password = utils.hash(random_password)
        try:
            site_id = dbquery.register_site(
                collection_site=main.cs,
                admin_id=admin_id,
                email=data.email,
                password=hashed_password,
                location=data.location,
                total_capacity=data.totalCapacity,
                longitude=data.longitude,
                latitude=data.latitude,
            )

        except errors.DuplicateKeyError as ex:
            response.status_code = status.HTTP_409_CONFLICT
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"email '{data.email}'already exists",
            )

        return {
            "msg": "site registraion successful",
            "siteId": site_id,
            "email": data.email,
            "password": random_password,
        }

    except Exception as ex:
        response.status_code = status.HTTP_409_CONFLICT
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.post("/site-login", status_code=status.HTTP_200_OK)
async def site_login(data: schemas.SiteLogin, response: Response):
    print(data.email)
    print(data.password)

    site = dbquery.site_login(main.cs, email=data.email)

    if not site: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    
    hashed_password = site.get("password")
    result = utils.verify(data.password, hashed_password)
    if not result: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    
    access_token = oauth.create_access_token({"email": site.get("email")})
    
    return {"access_token": access_token, "token_type": "bearer",}
    


@router.post("/site-login", status_code=status.HTTP_200_OK)
async def site_login(data: schemas.SiteLogin, response: Response):
    print(data.email)
    print(data.password)

    site = dbquery.site_login(main.cs, email=data.email)

    if not site: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    
    hashed_password = site.get("password")
    result = utils.verify(data.password, hashed_password)
    if not result: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    
    access_token = oauth.create_access_token({"email": site.get("email")})
    
    return {"access_token": access_token, "token_type": "bearer",}