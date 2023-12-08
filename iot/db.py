from pymongo import MongoClient
from icecream import ic
from datetime import datetime


def create_db(client):
    try:
        database_name = "CoffeeShop"

    # Create or access the specified database
        existing_db = client[database_name]

    # Insert a document into a collection (this will create the database if it doesn't exist)
        collection_users = existing_db["Users"]
        collection_sites = existing_db["Sites"]
        collection_data = existing_db["Data"]
        return collection_users,collection_sites,collection_data
    except Exception as e:
        print(f"Error: {e}")

# Create collections in the existing database


# Create or access the specified database
# db = client[database_name]
# print(client.list_database_names())
# UserID
# Brand Name
# Customer email address(User name)
# Password
# Location



# DataID
# UserID
# Site ID
# Timestamp
# Number of people inside
# Total trafic
# Total male
# Total female
# Total kids

# def add(cu,cs,cd):
#     cu.insert_one({"UserID": 1, "BrandName": "Starbucks", "CustomerEmail": "example@gmail.com", "Password": "1234", "Location": "F-10, Islamabad" })
#     cs.insert_one({"UserID": 1, "SiteID": "1_10", "Location": "F-9, Park, Islamabad" })
#     cd.insert_one({"DataID": 1, "SiteID": "1_10", "UserID":1, "TimeStamp": datetime.now() , "NoOfPeople": "10", "Totaltrafic":"12",
#                     "TotalMale": 2, "TotalFemale": 6, "TotalKids": 2 })


def main():
    client = MongoClient("mongodb://localhost:27017/")
    cu,cs,cd = create_db(client)
    return cu,cs,cd


def add_site(cs, user_id,  location):
    inserted_record = cs.insert_one({"UserID": user_id, "Location": location })
    return str(inserted_record.inserted_id)


if __name__ == "__main__": 
    client = MongoClient("mongodb://localhost:27017/")
    cu,cs,cd = create_db(client)
    result = add_site(cs, "25", "Islamabad")
    ic(result)
    # add(cu,cs,cd)