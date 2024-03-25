from fastapi import status, APIRouter, Response, Depends, HTTPException
from icecream import ic
from utils import oauth, password_manager
from db import db_query
import app
import datetime
from bson import ObjectId
from schemas import schemas

router = APIRouter(tags=["user-management"], prefix="/user")


@router.post(
    "/profile", status_code=status.HTTP_200_OK, response_model=schemas.ProfileRET
)
async def profile(response: Response, user_data=Depends(oauth.get_current_user)):
    ic(user_data)
    email = user_data[0]
    id = user_data[1]
    query_dict = {"_id": ObjectId(id), "email": email, "active": True}
    result = db_query.find_single_record(app.col_user, data_dict=query_dict)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )


@router.put("/profile", status_code=status.HTTP_200_OK)
async def update_password(
    response: Response,
    passwords: schemas.Password,
    user_data=Depends(oauth.get_current_user),
):
    ic(user_data)
    email = user_data[0]
    id = user_data[1]
    query_dict = {"_id": ObjectId(id), "email": email, "active": True}
    query_result = db_query.find_single_record(app.col_user, data_dict=query_dict)

   #  if user exists
    if query_result:
        # check current password is same as stored password or not
        pass_result = password_manager.verify(
            passwords.currentPassword, query_result.get("password")
        )

        # if current password and stored password is same
        if pass_result:
            # current and new passwords are same
            if passwords.currentPassword == passwords.newPassword:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="current password should not be same as new password",
                )

            # when current password and new password are not same
            else:
                query_dict = {
                    "_id": ObjectId(id),
                    "$set": {
                        "password": password_manager.hash(passwords.newPassword),
                        "updatedAt": datetime.datetime.now(datetime.UTC),
                    },
                }
                query_result = db_query.update_single_record(app.col_user, query_dict)
                if query_result:
                    return {"detail": "password updated successfully"}

        else:
            # if current password and stored passwords are not same
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="current password is not valid",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
