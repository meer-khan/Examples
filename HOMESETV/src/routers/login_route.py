from fastapi import status, APIRouter, Response, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from db import db_query
from utils import oauth, password_manager
from icecream import ic
import app

router = APIRouter(tags=["login"], prefix="/user")

@router.post("/login", status_code=status.HTTP_200_OK)
async def login( response: Response, user_credentials: OAuth2PasswordRequestForm = Depends()):
   try: 
      ic(user_credentials)
      user:dict = db_query.find_user(app.col_user, user_credentials.username)
      ic(user)
      if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
      
      else:
         result = password_manager.verify(user_credentials.password, user.get("password"))
         if not result: 
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail= "user not found"
                )
         else:
            access_token = oauth.create_access_token(
                {"email": user.get("email"), "id": str(user.get("_id"))}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "role": user.get("role")
            }

   except Exception as ex:   
      # TODO: LOG - C {ex}
      response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
      return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "internal server error"
        )





# @router.post("/login", status_code=status.HTTP_200_OK)
# async def site_login(data: schemas.Login, response: Response):
#     try:
#         site = dbquery.site_login(main.cs, email=data.email)
#         admin = dbquery.admin_login(main.ca, email=data.email)

#         if site:
#             hashed_password = site.get("password")
#             result = utils.verify(data.password, hashed_password)
#             if not result:
#                 response.status_code = status.HTTP_401_UNAUTHORIZED
#                 return HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
#                 )

#             access_token = oauth.create_access_token(
#                 {"email": site.get("email"), "id": str(site.get("_id"))}
#             )

#             return {
#                 "access_token": access_token,
#                 "token_type": "bearer",
#                 "role": "manager"
#             }
        
#         elif admin:
#             hashed_password = admin.get("password")
#             pass_verify = utils.verify(data.password, hashed_password)

#             if not pass_verify:
#                 response.status_code = status.HTTP_401_UNAUTHORIZED
#                 return HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
#                 )

#             access_token = oauth.create_access_token(
#                 {"email": admin.get("email"), "id": str(admin.get("_id"))}
#             )

#             return {
#                 "access_token": access_token,
#                 "token_type": "bearer",
#                 "role": "admin"
#             }
        
#         else:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_CREDENTIALS
#             )
        
#     except Exception as ex:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
#         )
    