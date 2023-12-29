from pymongo import MongoClient
from icecream import ic
from datetime import datetime, timedelta
from bson import ObjectId
import db, pytz

def db_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CoffeeShop"]
    data = db["Data"]
    return  data

def insert_many_record(collection,records):
    
    result = collection.insert_one(records)
    
    print(result)



if __name__ == "__main__": 
    data = db_connection()
    saudi_arabia_timezone = pytz.timezone("Asia/Riyadh")
    # utc = datetime.utcnow()
    # ic(utc)
    ct = datetime.utcnow().astimezone(saudi_arabia_timezone)
    ic(ct)
    record = {
    "userID": "6570de2e035bd03d6792503e",
    "location": "Lahore, Hall Road", 
    "total_capacity": 200,
    "noOfPeople": 10,
    "totalTraffic": 10,
    "totalMale":5,
    "totalFemale":4,
    "totalKids":1 ,
    "TimeStamp" : ct
    }
    retrieved_document = data.find_one({"_id": ObjectId("658ebfb5c0a3dbc6b271501f")})
    ic(retrieved_document)
    retrieved_timestamp_utc = retrieved_document["TimeStamp"]
    retrieved_timestamp_sa = retrieved_timestamp_utc.astimezone(saudi_arabia_timezone)
    ic(retrieved_timestamp_sa)
    # ic(record)
    # insert_many_record(data, record )