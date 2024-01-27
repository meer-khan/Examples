from pymongo import MongoClient
from icecream import ic
from datetime import datetime
from bson import ObjectId
import hashlib
import pytz


def add_user(cu, brand_name, customer_email, password, location):
    inserted_record = cu.insert_one(
        {
            "UserID": 1,
            "BrandName": brand_name,
            "CustomerEmail": customer_email,
            "Password": hashlib.sha256(str(password).encode()).hexdigest(),
            "Location": location,
        }
    )
    return str(inserted_record.inserted_id)


def add_site(cs, user_id, location, total_capacity):
    inserted_record = cs.insert_one(
        {"UserID": user_id, "Location": location, "TotalCapacity": total_capacity}
    )
    return str(inserted_record.inserted_id)


def add_data(
    cd,
    site_id,
    user_id,
    no_of_people,
    total_traffic,
    total_male,
    total_female,
    total_kids,
):
    # sa_tz = pytz.timezone('Asia/Riyadh')
    # local_time = datetime.now(sa_tz)
    # ic(local_time)
    # Convert local time to UTC
    # utc_time = local_time.astimezone(pytz.utc)
    cd.insert_one(
        {
            "DataID": 1,
            "SiteID": site_id,
            "UserID": user_id,
            "TimeStamp": datetime.utcnow(),
            "NoOfPeople": no_of_people,
            "Totaltrafic": total_traffic,
            "TotalMale": total_male,
            "TotalFemale": total_female,
            "TotalKids": total_kids,
        }
    )


def get_one_user(cu, user_id):
    ic(user_id)
    found_user = cu.find_one({"_id": ObjectId(user_id)})

    if found_user:
        return found_user
    else:
        return None


def get_users(cu):
    users = []
    all_users = cu.find({}, {"Password": 0, "UserID": 0})
    for user in all_users:
        # ic(type(user))
        # ic(str(user.get("_id")))
        user["_id"] = str(user.get("_id"))
        users.append(user)

    # print(users)
    return users


def add_queue_serving_time(qst, site_id, queue_serving_time, total_individuals):
    qst.insert_one(
        {
            "SiteID": site_id,
            "queueServingTime": queue_serving_time,
            "totalIndividuals": total_individuals,
            "createdAt": datetime.utcnow(),
        }
    )


def add_counter_idol_time(cit, site_id, idol_time, bson_binary, b64_image):
    cit.insert_one(
        {
            "SiteID": site_id,
            "idolTime": idol_time,
            "createdAt": datetime.utcnow(),
            "bsonBinImage": bson_binary,
            "b64Image": b64_image,
        }
    )


def add_customer_order_time(cot, site_id, customer_order_time):
    cot.insert_one(
        {
            "SiteID": site_id,
            "customerOrderTime": customer_order_time,
            "createdAt": datetime.utcnow(),
        }
    )
