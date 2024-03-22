import pymongo 
from bson import ObjectId
from icecream import ic

def insert_records(collection, data:dict):
    inserted_record = collection.insert_one(data)
    return inserted_record

def find_user(collection, data_field:str): 
    record = collection.find_one({"email": data_field})
    return record

def update_records(collection, id:str, **kwargs):
    updated_record = collection.update_one({"_id": ObjectId(id), "$set": kwargs})
    return updated_record