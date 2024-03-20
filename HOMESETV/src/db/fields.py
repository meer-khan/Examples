import pymongo 
from bson import ObjectId
from datetime import datetime

users = {
  "_id": ObjectId("..."),
  "username": "user123",
  "password": "...", 
  "email": "user@example.com",
  "roles": ["user", "editor"], 
  "plan_id": ObjectId("..."),
  "created_at": datetime.now(),
  "updated_at": datetime.now(),
  "active": True
}

roles = {
  "_id": ObjectId("..."),
  "role": "user",
  "permissions": ["read"], 
  "created_at": datetime.now(),
  "updated_at": datetime.now()
}


plans ={
  "_id": ObjectId("..."),
  "name": "Basic Plan",
  "description": "Basic subscription plan with limited features",
  "price": 10.99, 
  "duration": 30, 
  "features": ["feature1", "feature2"], 
  "created_at": datetime.now(),
  "updated_at": datetime.now()
}