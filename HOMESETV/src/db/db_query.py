from icecream import ic
from typing_extensions import List, Dict

def insert_records(collection, data:Dict):
    inserted_record = collection.insert_one(data)
    return inserted_record

def find_user(collection, data_field:str): 
    record = collection.find_one({"email": data_field})
    return record

def find_single_record(collection,  data_dict:Dict): 
    record = collection.find_one(data_dict)
    return record

def find_multiple_records(collection, data_dict:Dict)-> List: 
    records_list = collection.find(data_dict)
    return records_list

def update_single_record(collection, data_dict:Dict):
    ic(type(collection))
    updated_record = collection.update_one(data_dict)
    return updated_record