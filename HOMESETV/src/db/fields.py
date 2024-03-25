import pymongo 
from bson import ObjectId
from datetime import datetime

users = {
  "_id": ObjectId("..."),
  "username": "user123",
  "password": "...", 
  "email": "user@example.com",
  "roles": ["user_ObjectId"], 
  "plan_id": ObjectId("..."),
  "termsConditions": bool,
  "createdAt": datetime.now(),
  "updatedAt": datetime.now(),
  "active": True # Open to discussion 
}

roles = {
  "_id": ObjectId("..."),
  "role": "user",
  "permissions": ["read"], 
  "createdAt": datetime.now(),
  "updatedAt": datetime.now()
}


plans ={
  "_id": ObjectId("..."),
  "name": "Basic Plan",
  "description": "Basic subscription plan with limited features",
  "price": 10.99, 
  "duration": 30, 
  "features": ["feature1", "feature2"], 
  "createdAt": datetime.now(),
  "updatedAt": datetime.now()
}