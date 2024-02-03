from pymongo import MongoClient
from icecream import ic
from datetime import datetime
from bson import ObjectId
from decouple import config


def create_db(client):
    try:
        database_name = "CoffeeShop"

        # Create or access the specified database
        existing_db = client[database_name]

        # Insert a document into a collection (this will create the database if it doesn't exist)
        collection_admin = existing_db["admin"]
        collection_sites = existing_db["sites"]
        collection_data = existing_db["data"]
        collection_queue_serving_time = existing_db["queueServingTime"]
        collection_counter_idol_time = existing_db["counterIdolTime"]
        collection_customer_order_time = existing_db["customerOrderTime"]

        return (
            collection_admin,
            collection_sites,
            collection_data,
            collection_queue_serving_time,
            collection_counter_idol_time,
            collection_customer_order_time,
            # test,
        )
    except Exception as e:
        print(f"Error: {e}")


def main():
    client = MongoClient(config("CONNMONGO"))
    ca, cs, cd, cqst, ccit, ccot = create_db(client)
    cs.create_index("email", unique= True)
    return ca, cs, cd, cqst, ccit, ccot


# def add_site(cs, user_id, location):
#     inserted_record = cs.insert_one({"UserID": user_id, "Location": location})
#     return str(inserted_record.inserted_id)


# def get_one_user(cu, user_id):
#     ic(user_id)
#     found_user = cu.find_one({"_id": user_id})
#     if found_user:
#         print(found_user)
#         return found_user
#     else:
#         print(found_user)
#         return None


# def db_connnection():
# # if __name__ == "__main__":
#     client = MongoClient("mongodb://localhost:27017/")
#     cu,cs,cd = create_db(client)
#     result = add_site(cs, "25", "Islamabad")
#     ic(result)
#     # add(cu,cs,cd)
#     get_one_user(cu, ObjectId("6570de6b3ef211653f6f8fb9"))

#     return cu,cs,cd
