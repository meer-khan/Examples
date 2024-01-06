from pymongo import MongoClient
from icecream import ic
from datetime import datetime, timedelta
from bson import ObjectId
import db, pytz

def db_connection():
    client = MongoClient("mongodb+srv://mongouser:Admin1234Admin@cluster0.pjwv8.mongodb.net/?retryWrites=true&w=majority")
    db = client["CoffeeShop"]
    data = db["Data"]
    return  data


if __name__ == "__main__":
    data = db_connection()
    start_date = datetime(2023, 12, 10, 11, 13, 52, 335000)
    end_date = datetime(2023, 12, 25, 10, 7, 29, 774000)
    # cursor = data.find({"TimeStamp" : {"$gte": start_date, "$lte": end_date}})
    print(data.count_documents({"TimeStamp" : {"$gte": start_date, "$lte": end_date}}))

    # Delete records matching the filter
    result = data.delete_many({"TimeStamp" : {"$gte": start_date, "$lte": end_date}})

    # Print the number of deleted documents
    print("Number of deleted documents:", result.deleted_count)
    # for cur in cursor:
        # ic(cur)
    
    # print(cursor.count())