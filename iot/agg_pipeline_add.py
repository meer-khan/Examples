from datetime import datetime, timedelta
import json, pytz
from pymongo import MongoClient
from icecream import ic

# Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["CoffeeShop"]
# cd = db["Data"]

# saudi_arabia_timezone = pytz.timezone("Asia/Riyadh")

    # Calculate the start time for the last 24 hours in AST


# Construct the aggregation pipeline
def hourly_visits_last_24h(collection):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    pipeline_hourly_visits = [
            {
                "$match": {
                    "TimeStamp": {"$gte": start_time, "$lt": end_time}
                }
            },
            {
                "$group": {
                    "_id": {"hour": {"$hour": "$TimeStamp"}},
                    "NoOfPeople": {"$sum": "$NoOfPeople"}
                }
            },
            {
                "$sort": {"_id.hour": 1}
            }
        ]


    # Execute the aggregation pipeline

    # Format the result into JSON
    result_hourly_visits = list(collection.aggregate(pipeline_hourly_visits))

    formatted_result = [{"hour": entry["_id"]["hour"], "NoOfPeople": entry["NoOfPeople"]} for entry in result_hourly_visits]

        # Convert formatted result to JSON
    # json_result = json.dumps(formatted_result, default=str)
    # Convert result to JSON
    # json_result = json.dumps(result_hourly_visits, default=str)

    # return json_result/

    # Convert the result to JSON
    json_response = {"hourlyVisits": formatted_result}
    # print(json_result)
    return json_response
# json_result = json.dumps(formatted_result, indent=2)

# Print or pass the JSON result to your API
# print(json_result)



def calculate_daily_visits_for_last_7d(collection):
    current_utc_time = datetime.utcnow()

    # Calculate the start time for the last 7 days
    start_time_last_7_days = current_utc_time - timedelta(days=7)

    # Aggregation pipeline for daily visits in the last 7 days
    pipeline_daily_visits_last_7_days = [
        {
            "$match": {
                "TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}
            }
        },
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$TimeStamp"}},
                "total_visits": {"$sum": "$NoOfPeople"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "day": "$_id",
                "total_visits": 1
            }
        }
    ]

    # Execute the aggregation
    result_daily_visits_last_7_days = list(collection.aggregate(pipeline_daily_visits_last_7_days))

    # Convert result to a dictionary with day names
    formatted_result = {entry["day"]: entry["total_visits"] for entry in result_daily_visits_last_7_days}

    # Convert formatted result to JSON
    # json_result = json.dumps(formatted_result, default=str)
    json_response = {"dailyVisits": formatted_result}

    # ic(json_result)
    return json_response


# calculate_daily_visits_for_last_7d(collection=cd)



# utc_time_str = "2023-12-23T17:40:32.588+00:00"
# utc_time = datetime.fromisoformat(utc_time_str[:-6])  # Convert string to datetime, removing the offset


# pakistan_timezone = pytz.timezone("Asia/Karachi")
# pst_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pakistan_timezone)


# pst_time_str = pst_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
# print(pst_time_str)

# sa_tz = pytz.timezone('Asia/Riyadh')
# local_time = datetime.now(sa_tz)
# ic(local_time)


# client.close()