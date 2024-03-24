from fastapi import status, APIRouter, Response, Depends
from icecream import ic
from utils import oauth
from db import db_query
import app
from bson import ObjectId
from schemas import schemas
router = APIRouter(tags=["profile"])

@router.post("/profile", status_code=status.HTTP_200_OK, response_model=schemas.ProfileRET)
async def profile(response: Response, user_data = Depends(oauth.get_current_user)):
   ic(user_data)
   email = user_data[0]
   id = user_data[1]
   quer_dict = {"_id": ObjectId(id), "email": email}
   result = db_query.find_single_record(app.col_user, data_dict=quer_dict)
   ic(result)
   return result