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
async def profile(response: Response, user_data:dict=Depends(oauth.get_current_user)):

    query_dict = {"_id": ObjectId(user_data.get("sub")), "active": True, "passVer": user_data.get("ver")}
    result = db_query.find_single_record(app.col_user, data_dict=query_dict)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

# Change password
@router.put("/profile", status_code=status.HTTP_200_OK)
async def update_password(
   response: Response,
   passwords: schemas.Password,
   user_data:dict=Depends(oauth.get_current_user),
   ):
   query_dict = {"_id": ObjectId(user_data.get("sub")), "active": True, "passVer": user_data.get("ver")}
   query_result:dict = db_query.find_single_record(app.col_user, data_dict=query_dict)

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
               filter_query ={"_id": ObjectId(user_data.get("sub"))}
               query_dict = {
                  "$set": {
                     "active"
                  },
                  "$inc": {"passVer": 1} 
               }
               query_result = db_query.update_single_record(app.col_user, filter_query, query_dict)
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





# Delete Profile
@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
   response: Response,
   data: schemas.DelAccount,
   user_data:dict=Depends(oauth.get_current_user),
   ):
   query_dict = {"_id": ObjectId(user_data.get("sub")), "active": True, "passVer": user_data.get("ver")}
   query_result:dict = db_query.find_single_record(app.col_user, data_dict=query_dict)

   #  if user exists
   if query_result:
      # check current password is same as stored password or not
      pass_result = password_manager.verify(
         data.password, query_result.get("password")
      )

      # if current password and stored password is same -> delete the user
      if pass_result:
         # query to set the active status of account as False
               filter_query =  {"_id": ObjectId(user_data.get("sub"))}
               query_dict = {"$set": {"active": False}}
               db_query.update_single_record(app.col_user, filter_query, query_dict)
               return {
                   "detail": "account deleted successfully"
               }
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
