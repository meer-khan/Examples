from pymongo import MongoClient
from icecream import ic
from datetime import datetime
from bson import ObjectId
import db


def insert_many_record(collection,records):
    result = collection.insert_many(records)
    
    print(result)



if __name__ == "__main__": 
     au, books, data = db.db_connection()


#      records = [
#     {
#       "_id": 100,
#       "name": "F. Scott Fitzgerald",
#       "birth_year": 1896
#     },
#     {
#       "_id": 101,
#       "name": "George Orwell",
#       "birth_year": 1903
#     },
#     {
#       "_id": 102,
#       "name": "Harper Lee",
#       "birth_year": 1926
#     }
#   ]
     
     records = []
     insert_many_record(data, )