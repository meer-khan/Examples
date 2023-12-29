from pymongo import MongoClient
from icecream import ic
from datetime import datetime
from bson import ObjectId
import db


def db_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CoffeeShop"]
    data = db["Data"]
    return  data


def update(collection):
    pipeline = [
    {
        "$set": {
            "TimeStamp": {
                "$dateToString": {
                    "date": "$TimeStamp",
                    "format": r"%Y-%m-%dT%H:%M:%S.%L"  # Adjust the format based on your requirement
                }
            }
        }
    }
]

# Update all records in the collection
    result = collection.update_many({}, pipeline)
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")
    # collection.update_one()



if __name__ == "__main__":
    data = db_connection()
    update(data)