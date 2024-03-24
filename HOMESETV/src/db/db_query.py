import pymongo 
from bson import ObjectId
from icecream import ic
from typing_extensions import List

def insert_records(collection, data:dict):
    inserted_record = collection.insert_one(data)
    return inserted_record

def find_user(collection, data_field:str): 
    record = collection.find_one({"email": data_field})
    return record

def find_single_record(collection,  data_dict:dict): 
    record = collection.find_one(data_dict)
    return record

def find_multiple_records(collection, data_dict)-> List: 
    records_list = collection.find(data_dict)
    return records_list

def update_records(collection, id:str, **kwargs):
    updated_record = collection.update_one({"_id": ObjectId(id), "$set": kwargs})
    return updated_record