from pymongo import MongoClient
from icecream import ic
from datetime import datetime


def add_user(cu,cs,cd):
    cu.insert_one({"UserID": 1, "BrandName": "Starbucks", "CustomerEmail": "example@gmail.com", "Password": "1234", "Location": "F-10, Islamabad" })
    

def add_site(cs, user_id,  location):
    inserted_record = cs.insert_one({"UserID": user_id, "Location": location })
    return str(inserted_record.inserted_id)

def add_data(cd,data):
    cd.insert_one({"DataID": 1, "SiteID": "1_10", "UserID":1, "TimeStamp": datetime.now() , "NoOfPeople": "10", "Totaltrafic":"12",
                    "TotalMale": 2, "TotalFemale": 6, "TotalKids": 2 })

def get_one_user(cu, data):
    found_user = cu.find_one({"_id": data.get("id")})
    if found_user:
        return found_user
    else:
        return None


def get_users(cu):
    users = []
    all_users = cu.find()
    for user in all_users:
        # ic(type(user))
        # ic(str(user.get("_id")))
        user["_id"] = str(user.get("_id"))
        users.append(user)
    
    # print(users)
    return users