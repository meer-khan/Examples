import pymongo 
from bson import ObjectId
from icecream import ic
def insert_records(collection, data):
    ic("***********************")
    ic(data)
    inserted_record = collection.insert_one(data)
    return inserted_record

def update_records(collection, id, **kwargs):
    updated_record = collection.update_one({"_id": ObjectId(id), "$set": kwargs})
    return updated_record