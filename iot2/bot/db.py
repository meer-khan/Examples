from pymongo import MongoClient
from icecream import ic
from decouple import config

def create_db(client):
    try:
        database_name = config("DB_NAME")

        # Create or access the specified database
        existing_db = client[database_name]

        # Insert a document into a collection (this will create the database if it doesn't exist)
        collection_super_admin = existing_db["superAdmin"]
        collection_admin = existing_db["admin"]
        collection_sites = existing_db["sites"]
        collection_data = existing_db["Data"]
        collection_queue_serving_time = existing_db["queueServingTime"]
        collection_counter_idol_time = existing_db["counterIdolTime"]
        collection_customer_order_time = existing_db["customerOrderTime"]

        return (
            collection_super_admin,
            collection_admin,
            collection_sites,
            collection_data,
            collection_queue_serving_time,
            collection_counter_idol_time,
            collection_customer_order_time,
            
        )
    except Exception as e:
        print(f"Error: {e}")


def main():
    client = MongoClient(config("CONNMONGO"))
    csa, ca, cs, cd, cqst, ccit, ccot = create_db(client)
    # cs.create_index("email", unique= True)
    # ca.create_index("email", unique= True)

    return csa, ca, cs, cd, cqst, ccit, ccot