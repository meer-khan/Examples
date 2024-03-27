from icecream import ic
from typing_extensions import List, Dict
from pymongo.collection import Collection
from bson import ObjectId



class Queries:
    def get_find_user_query_dict(self, id:str, pass_version:str, active_status:bool)-> Dict:
        return {"_id": ObjectId(id), "active": active_status, "passVer": pass_version}




def insert_records(collection:Collection, data:Dict):
    inserted_record = collection.insert_one(data)
    return inserted_record

def find_user(collection:Collection, data_field:str): 
    record = collection.find_one({"email": data_field})
    return record

def find_single_record(collection:Collection,  data_dict:Dict): 
    record = collection.find_one(data_dict)
    return record

def find_multiple_records(collection:Collection, data_dict:Dict)-> List: 
    records_list = collection.find(data_dict)
    return records_list

def update_single_record(collection:Collection, filter_dict:Dict, update_dict:Dict):
    updated_record = collection.update_one(filter_dict,update_dict)
    ic(type(updated_record))
    return updated_record

