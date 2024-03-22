from fastapi import status, APIRouter, Response, HTTPException
from icecream import ic
from pymongo import errors
import sys
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
# print(BASE_DIR)
sys.path.append(str(BASE_DIR))
ic(sys.path)
from schemas import schemas
import app
from db import db_query

router = APIRouter(tags=["signup"], prefix="/user")


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=dict)
async def signup(data: schemas.Signup, response: Response):
    try:
        user_data = data.model_dump()
        inserted_record = db_query.insert_records(collection=app.col_user, data=user_data)
        # TODO: Log - I
        return {"detail": "user registered successfully"}

    except errors.DuplicateKeyError:
        # TODO: Log - W
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists with this email",
        )

    except Exception: 
        # TODO: Log - C
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")

# @router.post("/registration", status_code=status.HTTP_201_CREATED)
# def admin_registration(
#     data: schemas.AdminRegistration,
#     response: Response,
#     token: str = Depends(main.oauth2_scheme),
# ):

#     result = oauth.get_current_user(token=token)

#     if isinstance(result, HTTPException):
#         response.status_code = status.HTTP_401_UNAUTHORIZED
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail= ExceptionLiterals.INVALID_TOKEN,
#         )
#     try:
#         user = dbquery.get_one_user(collection_user=main.csa, user_id=result.id)
#         if not user:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail= ExceptionLiterals.ID_NOT_FOUND,
#             )

#         # generate random password 5
#         # EcT/5~F\" 520@gmail
#         random_password = utils.generate_random_password(8)
#         hashed_password = utils.hash(random_password)
#         try:
#             admin_id = dbquery.add_admin(
#                 main.ca, email=data.email, password=hashed_password
#             )
#             return {
#                 "msg": SuccessLiterals.REGISTRATION_SUCCESSFUL,
#                 "adminId": admin_id,
#                 "email": data.email,
#                 "password": random_password,
#             }

#         except errors.DuplicateKeyError as ex:
#             response.status_code = status.HTTP_409_CONFLICT
#             return HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail= ExceptionLiterals.EMAIL_ALREADY_EXISTS + data.email,
#             )
#     except Exception as ex:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
#         )
