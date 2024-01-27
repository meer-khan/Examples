# from datetime import datetime, timedelta
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["CoffeeShop"]
# collection = db["Data"]

# # Get the current UTC time
# current_utc_time = datetime.utcnow()

# # Calculate the start time for the last 24 hours
# start_time_last_24_hours = current_utc_time - timedelta(hours=24)

# # Aggregation pipeline for the last 24 hours
# pipeline_last_24_hours = [
#     {
#         "$match": {
#             "TimeStamp": {"$gte": start_time_last_24_hours, "$lt": current_utc_time}
#         }
#     },
#     {
#         "$group": {
#             "_id": None,
#             "total_male": {"$sum": "$TotalMale"},
#             "total_female": {"$sum": "$TotalFemale"},
#             "total_kids": {"$sum": "$TotalKids"}
#         }
#     }
# ]

# # Execute the aggregation
# result_last_24_hours = list(collection.aggregate(pipeline_last_24_hours))

# # Print the result
# print(result_last_24_hours)




# # Calculate the start time for the last 7 days
# start_time_last_7_days = current_utc_time - timedelta(days=7)

# # Aggregation pipeline for the last 7 days
# pipeline_last_7_days = [
#     {
#         "$match": {
#             "TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}
#         }
#     },
#     {
#         "$group": {
#             "_id": None,
#             "total_male": {"$sum": "$TotalMale"},
#             "total_female": {"$sum": "$TotalFemale"},
#             "total_kids": {"$sum": "$TotalKids"}
#         }
#     }
# ]

# # Execute the aggregation
# result_last_7_days = list(collection.aggregate(pipeline_last_7_days))

# # Print the result
# print(result_last_7_days)




# # Calculate the start time for the last 30 days
# start_time_last_30_days = current_utc_time - timedelta(days=30)

# # Aggregation pipeline for the last 30 days
# pipeline_last_30_days = [
#     {
#         "$match": {
#             "TimeStamp": {"$gte": start_time_last_30_days, "$lt": current_utc_time}
#         }
#     },
#     {
#         "$group": {
#             "_id": None,
#             "total_male": {"$sum": "$TotalMale"},
#             "total_female": {"$sum": "$TotalFemale"},
#             "total_kids": {"$sum": "$TotalKids"}
#         }
#     }
# ]

# Execute the aggregation
# result_last_30_days = list(collection.aggregate(pipeline_last_30_days))

# # Print the result
# # print(result_last_30_days)

# result_last_7_days[0].pop("_id")
# result_last_24_hours[0].pop("_id")
# result_last_30_days[0].pop("_id")

# # print("____________________-")
# result = {"total_m_f_k_24h": result_last_24_hours[0], "total_m_f_k_7d": result_last_7_days[0], "total_m_f_k_30d": result_last_30_days[0]}
# # print(result)

# import pytz
# from icecream import ic
# sa_tz = pytz.timezone('Asia/Riyadh')
# local_time = datetime.now(sa_tz)
# fmt = "%Y-%m-%d %H:%M"
# ic(local_time.strftime(fmt))
# # Convert local time to UTC
# utc_time = local_time.astimezone(pytz.utc)
# ic(datetime.utcnow().strftime(fmt))
# ic(utc_time.strftime(fmt))



# ic(utc_time)
# ic(datetime.now())
# ic(local_time)




from datetime import datetime, timedelta
from pymongo import MongoClient
from icecream import ic

# Connect to MongoDB
# client = MongoClient("mongodb+srv://mongouser:Admin12345admin@cluster0.pjwv8.mongodb.net/?retryWrites=true&w=majority")
# db = client["CoffeeShop"]
# cd = db["Data"]

# print("Getting records")
# query = {"TotalMale":{"gte": 10000}}
# cursor = cd.find(query)
# print(cd.count_documents(query))


# # for record in cursor:
# #     print(record)




# client.close()



from pymongo import MongoClient
import pytz
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["CoffeeShop"]
collection = db["Data"]

# Rename the field for all documents
# collection.update_many({}, { "$rename": { "DateTime": "TimeStamp" } })
timezone = pytz.timezone("Asia/Riyadh")
# print(type(timezone))
end_time = datetime.now()
start_time = end_time - timedelta(days=15)
ic(start_time)

utc = datetime.utcnow()
ic(utc)
ct = datetime.now(timezone)
ic(ct)

# pipeline_hourly_visits = [
    
#             {
#                 "$match": {
#                     "TimeStamp": {"$gte": start_time, "$lt": end_time ,}
#                 }
#             },
#                 {"$project":
#                  {"dateToParts":
#                   {"$dateToParts":
#                    {"date":'$TimeStamp',"timezone":'Asia/Riyadh'}
#                    }
#                  },
#                  "TimeStamp": 1
#             },
                
            
#             {"$limit":1}
#         ]
# result_hourly_visits = list(collection.aggregate(pipeline_hourly_visits))
# print(result_hourly_visits)

# ic("***************")

# pipeline_hourly_visits = [

#             {
#                 "$match": {
#                     "TimeStamp": {"$gte": start_time, "$lt": end_time}
#                 }
#             },
                
            
#             {"$limit":1}
#         ]

# result_hourly_visits = list(collection.aggregate(pipeline_hourly_visits))
# print(result_hourly_visits)
# Close the connection
client.close()




# di = {"hour": 1, "hour2": 3}

# di.update({"hour3": 7})
# print(di)


d = [1,2,None]
print(all(d))