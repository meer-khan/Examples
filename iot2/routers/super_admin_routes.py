from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pymongo import errors
from typing import List
from icecream import ic
from bson import ObjectId
import dbquery
import oauth
import schemas
import utils
import main

router = APIRouter(tags=["Admin Routes"], prefix="/super-admin")




@router.post("/register")
async def super_admin_registration(): 
    email= "shahmirkhan519@gmail.com"
    password = "Pakistan2212"
    hashed_password = utils.hash(password)
    result = dbquery.add_super_admin(main.csa, email, hashed_password)
    ic(result)
    return {"msg": "Super Admin Registration Successful"}







@router.post("/login", status_code=status.HTTP_200_OK)
async def admin_login(data: schemas.Login, response: Response):

    admin = dbquery.admin_login(main.csa, email=data.email)
    
    if not admin:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )

    hashed_password = admin.get("password")
    pass_verify = utils.verify(data.password, hashed_password)

    if not pass_verify:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )

    access_token = oauth.create_access_token(
        {"email": admin.get("email"), "id": str(admin.get("_id"))}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }




@router.get(
    "/profile", status_code=status.HTTP_200_OK, response_model= List[schemas.AdminProfile]
)
async def admin_profile(response: Response, token:str = Depends(main.oauth2_scheme)):

    result = oauth.get_current_user(token=token)

    if isinstance(result, HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials: Token Expired- Try Login again"
        )
    
    admin = dbquery.get_admin(main.ca, result.email, result.id)

    if admin: 
        results = dbquery.get_admin_data(main.cs)
        data = []
        for document in results: 
            _id = document.pop("_id")
            document.update({"id": str(_id)})

            data.append(document)

        ic(data)
        return data
    
    return  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data not Found"
        )