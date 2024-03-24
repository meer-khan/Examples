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


# @router.post("/refresh-token", status_code=status.HTTP_200_OK)
# async def refresh_token(refreshToken:str, response: Response):
#    try: 
#       id = oauth.verify_refresh_token(refreshToken)
#       user:dict = db_query.find_user(app.col_user, data_field=, data)
#       ic(user)
#       if not user:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
      
#       else:
#          result = password_manager.verify(user_credentials.password, user.get("password"))
#          if not result: 
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED, detail= "user not found"
#                 )
#          else:
#             access_token = oauth.create_access_token(
#                 {"email": user.get("email"), "id": str(user.get("_id"))}
#             )

#             return {
#                 "access_token": access_token,
#                 "token_type": "bearer",
#                 "role": user.get("role")
#             }

#    except Exception as ex:   
#       # TODO: LOG - C {ex}
#       response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#       return HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "internal server error"
#         )