from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pymongo import errors
from typing import List
from icecream import ic
from message_literals.messages import ExceptionLiterals, SuccessLiterals
import dbquery
import oauth
import schemas
import utils
import main

router = APIRouter(tags=["Admin Routes"], prefix="/admin")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def admin_registration(
    data: schemas.AdminRegistration,
    response: Response,
    token: str = Depends(main.oauth2_scheme),
):

    result = oauth.get_current_user(token=token)

    if isinstance(result, HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= ExceptionLiterals.INVALID_TOKEN,
        )
    try:
        user = dbquery.get_one_user(collection_user=main.csa, user_id=result.id)
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= ExceptionLiterals.ID_NOT_FOUND,
            )

        # generate random password 5
        # EcT/5~F\" 520@gmail
        random_password = utils.generate_random_password(8)
        hashed_password = utils.hash(random_password)
        try:
            admin_id = dbquery.add_admin(
                main.ca, email=data.email, password=hashed_password
            )
            return {
                "msg": SuccessLiterals.REGISTRATION_SUCCESSFUL,
                "adminId": admin_id,
                "email": data.email,
                "password": random_password,
            }

        except errors.DuplicateKeyError as ex:
            response.status_code = status.HTTP_409_CONFLICT
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= ExceptionLiterals.EMAIL_ALREADY_EXISTS + data.email,
            )
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )

@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.AdminProfileSites],
)
async def admin_profile(response: Response, token: str = Depends(main.oauth2_scheme)):
    try: 
        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= ExceptionLiterals.INVALID_TOKEN,
            )

        admin = dbquery.get_admin(main.ca, result.email, result.id)

        if admin:
            results = dbquery.get_admin_data(main.cs, result.id)
            data = []
            for document in results:
                _id = document.pop("_id")
                document.update({"_id": str(_id)})

                data.append(document)
            return data

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail= ExceptionLiterals.ID_NOT_FOUND
            )
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.get(
    "/profile/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.SiteProfile
    | None,  # None is used to protect to display results of site with valid admin token but site id is not registered with admin id - Say Thanks
)
async def admin_profile_site_by_id(
    id: str, response: Response, token: str = Depends(main.oauth2_scheme)
):
    
    try:
        result = oauth.get_current_user(token=token)
        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= ExceptionLiterals.INVALID_TOKEN,
            )

        admin = dbquery.get_admin(main.ca, result.email, result.id)

        if admin:
            results = dbquery.get_site(main.cs, site_id=id, admin_id=result.id)
            return results

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail= ExceptionLiterals.ID_NOT_FOUND
            )
    
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )




# REMOVED ROUTE



# @router.post("/login", status_code=status.HTTP_200_OK)
# async def admin_login(data: schemas.Login, response: Response):

#     try:

#         admin = dbquery.admin_login(main.ca, email=data.email)

#         if not admin:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
#             )

#         hashed_password = admin.get("password")
#         pass_verify = utils.verify(data.password, hashed_password)

#         if not pass_verify:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
#             )

#         access_token = oauth.create_access_token(
#             {"email": admin.get("email"), "id": str(admin.get("_id"))}
#         )

#         return {
#             "access_token": access_token,
#             "token_type": "bearer",
#         }
#     except Exception as ex:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
#         )

