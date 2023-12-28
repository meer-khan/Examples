from pymongo import MongoClient
from icecream import ic
from datetime import datetime
from bson import ObjectId


def db_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Agree"]
    au = db["authors"]
    books = db["books"]
    data = db["data"]
    print(type(au))
    return au, books, data

