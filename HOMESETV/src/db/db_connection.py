from pymongo import MongoClient, errors
from decouple import config
from datetime import datetime
from icecream import ic

def create_db_connection(connection_string: str, db_name: str):
    """
    create database connection
    """
    client = MongoClient(connection_string)
    db = client[db_name]

    return db


def create_db_collections(collection_users, collection_roles, collections_plans, db):
    """
    Create a new collection in the database.
    """
    try:
        # col_user = db.create_collection(collection_users)
        # col_roles = db.create_collection(collection_roles)
        # col_roles = db.create_collection(collections_plans)
        col_user = db[collection_users]
        col_roles = db[collection_roles]
        col_plans = db[collections_plans]
        return col_user, col_roles, col_plans
    
    except errors.CollectionInvalid as ex:
        raise ex

def find_role(collection):
    admin = collection.find_one({"role": "admin"})
    user = collection.find_one({"role": "user"})
    return admin, user


def add_roles(collection): 
    
    collection.insert_one({"role": "user", "permissions": ["create", "read", "update", "delete"], "createdAt": datetime.now(), "updatedAt": datetime.now()})
    collection.insert_one({"role": "admin", "permissions": ["create", "read", "update", "delete"], "createdAt": datetime.now(), "updatedAt": datetime.now()})

def db_creation():
    """
    main function to create database and collections
    """
    users_collection = "users"
    roles_collection = "roles"
    plans_collection = "plans"
    db_name = config("DB_NAME")
    db_conn_str = config("DB_CONN_STR")

    db_instance = create_db_connection(db_conn_str, db_name)

    col_user, col_roles, col_plans = create_db_collections(
        collection_users=users_collection,
        collection_roles=roles_collection,
        collections_plans=plans_collection,
        db=db_instance,
    )

    admin, user = find_role(col_roles)
    if (admin and user) is None:
        add_roles(collection=col_roles)

    col_user.create_index("email", unique= True)
    col_roles.create_index("role", unique= True)
    return col_user, col_roles, col_plans
