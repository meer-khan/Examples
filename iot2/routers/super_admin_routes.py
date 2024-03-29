from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import List, Union
from icecream import ic
from message_literals.messages import ExceptionLiterals, SuccessLiterals
import dbquery
import oauth
import schemas
import utils
import main

router = APIRouter(tags=["Admin Routes"], prefix="/super-admin")


# @router.post("/register")
# async def super_admin_registration():
#     email= "shahmirkhan519@gmail.com"
#     password = "Pakistan2212"
#     hashed_password = utils.hash(password)
#     result = dbquery.add_super_admin(main.csa, email, hashed_password)
#     ic(result)
#     return {"msg": "Super Admin Registration Successful"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def admin_login(data: schemas.Login, response: Response):
    try:
        admin = dbquery.admin_login(main.csa, email=data.email)

        if not admin:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionLiterals.INVALID_CREDENTIALS,
            )

        hashed_password = admin.get("password")
        pass_verify = utils.verify(data.password, hashed_password)

        if not pass_verify:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionLiterals.INVALID_CREDENTIALS,
            )

        access_token = oauth.create_access_token(
            {"email": admin.get("email"), "id": str(admin.get("_id"))}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "super_admin"
        }

    except HTTPException as ex:
        raise HTTPException(status_code= response.status_code , detail=str(ex))
    
    except Exception as ex: 
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(ex))


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.AdminProfile],
)
async def super_admin_profile(
    response: Response, token: str = Depends(main.oauth2_scheme)
):

    try:

        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionLiterals.INVALID_TOKEN,
            )

        admin = dbquery.get_admin(main.csa, result.email, result.id)
        ic(admin)
        if admin:
            results = dbquery.get_all_admins(main.ca)
            data = []
            for document in results:
                document["id"] = str(document.get("_id"))
                data.append(document)
            return data

        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ExceptionLiterals.ID_NOT_FOUND
        )

    except HTTPException as ex:
        raise HTTPException(status_code=response.status_code, detail=str(ex))

    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(ex))


@router.get(
    "/profile/{admin_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.SAAdminSitesRet],
)
async def super_admin_profile(
    admin_id, response: Response, token: str = Depends(main.oauth2_scheme)
):

    try:

        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionLiterals.INVALID_TOKEN,
            )

        sites = dbquery.super_admin_get_sites_of_admin(main.cs, admin_id)

        if sites:
            data = []
            for document in sites:
                document["_id"] = str(document.get("_id"))
                data.append(document)
            return data
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ExceptionLiterals.ID_NOT_FOUND
        )

    except HTTPException as ex:
        raise HTTPException(status_code=response.status_code, detail=str(ex))

    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(ex))


@router.put("/profile/{site_id}/{field_name}")
async def admin_profile_update(
    site_id: str,
    field_name: str,
    response: Response,
    token: str = Depends(main.oauth2_scheme),
):
    try:
        # Validate field_name
        valid_fields = ["active_status", "show_data"]
        if field_name not in valid_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field_name. Supported fields: {valid_fields}",
            )

        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionLiterals.INVALID_TOKEN,
            )

        super_admin = dbquery.get_admin(main.csa, result.email, result.id)
        if super_admin:
            updated_site, toggled_value = dbquery.update_site(
                main.cs, field_name=field_name, site_id=site_id
            )
            if updated_site.modified_count:
                return {
                    "message": f"{field_name} toggled for item {site_id}",
                    "value": toggled_value,
                }

        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ExceptionLiterals.ID_NOT_FOUND
        )

    except HTTPException as ex:
        raise HTTPException(status_code= response.status_code , detail=str(ex))
    
    except Exception as ex: 
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=500, detail=str(ex))
