from fastapi import status, APIRouter, Response, HTTPException, Form
from icecream import ic
from pydantic import ValidationError
from pymongo import errors
from schemas import schemas
import app
from db import db_query
import sys

# ic(sys.path)
from utils import password_manager

router = APIRouter(tags=["signup"], prefix="/user")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    response: Response,
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(...),
    phoneNo: str = Form(...),
    termsConditions: bool = Form(...),
):
    try:
        user_data = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password1": password1,
            "password2": password2,
            "phoneNo": phoneNo,
            "termsConditions": termsConditions,
        }
        ic(user_data)
        try:
            user_data = schemas.Signup(
                
                    firstName= firstName,
                    lastName= lastName,
                    email=  email,
                    password1= password1,
                    password2=  password2,
                    phoneNo = phoneNo,
                    termsConditions = termsConditions,
                
            )
        except ValidationError as exc_info:
            ic(exc_info)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc_info.errors())

        user_data = user_data.model_dump()
        user_data["password"] = password_manager.hash(user_data["password1"])
        user_data.pop("password1")
        user_data.pop("password2")
        user_data.update({"roles": ["user"], "plan": None})
        ic(user_data)
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
