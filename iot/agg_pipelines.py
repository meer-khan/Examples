from datetime import datetime, timedelta
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["CoffeeShop"]
collection = db["Data"]

# Get the current UTC time
current_utc_time = datetime.utcnow()

# Calculate the start time for the last 24 hours
start_time_last_24_hours = current_utc_time - timedelta(hours=24)
start_time_previous_24_hours = start_time_last_24_hours - timedelta(hours=24)

# Calculate the start time for the last 7 days
start_time_last_7_days = current_utc_time - timedelta(days=7)
start_time_previous_7_days = start_time_last_7_days - timedelta(days=7)




# Aggregation pipeline for the last 24 hours
pipeline_last_24_hours = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_24_hours, "$lt": current_utc_time}
        }
    },
    {
        "$group": {
            "_id": None,
            "user_count_last_24_hours": {"$sum": "$NoOfPeople"}
        }
    }
]

pipeline_previous_24_hours = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_previous_24_hours, "$lt": start_time_last_24_hours}
        }
    },
    {
        "$group": {
            "_id": None,
            "user_count_previous_24_hours": {"$sum": "$NoOfPeople"}
        }
    }
]

# Aggregation pipeline for the last 7 days
pipeline_last_7_days = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}
        }
    },
    {
        "$group": {
            "_id": None,
            "user_count_last_7_days": {"$sum": "$NoOfPeople"}
        }
    }
]


pipeline_previous_7_days = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_previous_7_days, "$lt": start_time_last_7_days}
        }
    },
    {
        "$group": {
            "_id": None,
            "user_count_previous_7_days": {"$sum": "$NoOfPeople"}
        }
    }
]



# Execute the aggregations
result_last_24_hours = list(collection.aggregate(pipeline_last_24_hours))
result_previous_24_hours = list(collection.aggregate(pipeline_previous_24_hours))


result_last_7_days = list(collection.aggregate(pipeline_last_7_days))
result_previous_7_days = list(collection.aggregate(pipeline_previous_7_days))

# Extract the user counts
user_count_last_24_hours = result_last_24_hours[0]["user_count_last_24_hours"] if result_last_24_hours else 0
user_count_last_7_days = result_last_7_days[0]["user_count_last_7_days"] if result_last_7_days else 0
user_count_previous_24_hours = result_previous_24_hours[0]["user_count_previous_24_hours"] if result_previous_24_hours else 0
user_count_previous_7_days = result_previous_7_days[0]["user_count_previous_7_days"] if result_previous_7_days else 0
# Calculate the difference
user_count_difference = user_count_last_24_hours - user_count_previous_24_hours
# Print the results
print("Visitor Count Last 24 Hours:", user_count_last_24_hours)
print("Visitor Count Difference 24 Hours:", user_count_difference)
print("Visitor Count Last 7 Days:", user_count_last_7_days)
print("Visitor Count Previous 7 Days:", user_count_previous_7_days)




# Calculate the start time for the current day
start_time_current_day = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0)

# Aggregation pipeline for the current day
pipeline_current_day = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_current_day, "$lt": current_utc_time}
        }
    },
    {
        "$group": {
            "_id": None,
            "total_male_current_day": {"$sum": "$TotalMale"},
            "total_female_current_day": {"$sum": "$TotalFemale"},
            "total_kids_current_day": {"$sum": "$TotalKids"}
        }
    }
]


# Execute the aggregation
result_current_day = list(collection.aggregate(pipeline_current_day))

# Extract the totals
total_male_current_day = result_current_day[0]["total_male_current_day"] if result_current_day else 0
total_female_current_day = result_current_day[0]["total_female_current_day"] if result_current_day else 0
total_kids_current_day = result_current_day[0]["total_kids_current_day"] if result_current_day else 0

# Print the results
print("Total Male on Current Day:", total_male_current_day)
print("Total Female on Current Day:", total_female_current_day)
print("Total Kids on Current Day:", total_kids_current_day)








pipeline_avg_hourly_visitors = [
    {
        "$group": {
            "_id": {"$hour": "$TimeStamp"},
            "average_hourly_visitors": {"$avg": "$NoOfPeople"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

# Execute the aggregation
result_avg_hourly_visitors = list(collection.aggregate(pipeline_avg_hourly_visitors))

# Extract the results
result  = []
for entry in result_avg_hourly_visitors:
    id = entry["_id"] 
    av = entry["average_hourly_visitors"]
    {"hour": entry["_id"], "average_visitors": entry["average_hourly_visitors"]} 

average_hourly_visitors = [{"hour": entry["_id"], "average_visitors": int(entry["average_hourly_visitors"]) if entry["average_hourly_visitors"] != None else 0 } for entry in result_avg_hourly_visitors]

# Create a JSON response
json_response = {
    "average_hourly_visitors": average_hourly_visitors
}

print(json_response)








# Aggregation pipeline for average daily visitors
pipeline_avg_daily_visitors = [
    {
        "$group": {
            "_id": {"$dayOfWeek": "$TimeStamp"},
            "average_daily_visitors": {"$avg": "$NoOfPeople"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

# Execute the aggregation
result_avg_daily_visitors = list(collection.aggregate(pipeline_avg_daily_visitors))

# Extract the results
average_daily_visitors = [{"day_of_week": entry["_id"], "average_visitors": entry["average_daily_visitors"]} for entry in result_avg_daily_visitors]

# Map day_of_week values to day names
day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
average_daily_visitors_mapped = [{day_names[entry["day_of_week"] - 1]: entry["average_visitors"]} for entry in average_daily_visitors]

# Create a JSON response
json_response = {
    "average_daily_visitors": average_daily_visitors_mapped
}

# Print the JSON response
print(json_response)

# If you want to print the formatted JSON, you can use the following line instead:
# print(json.dumps(json_response, indent=2))
