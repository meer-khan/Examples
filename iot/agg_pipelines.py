from datetime import datetime, timedelta
from pymongo import MongoClient
from icecream import ic
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["CoffeeShop"]
collection = db["Data"]





def total_visit_last_24_hours():
    current_utc_time = datetime.utcnow()
    start_time_last_24_hours = current_utc_time - timedelta(hours=24)
    start_time_previous_24_hours = start_time_last_24_hours - timedelta(hours=24)
        
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

    result_last_24_hours = list(collection.aggregate(pipeline_last_24_hours))
    result_previous_24_hours = list(collection.aggregate(pipeline_previous_24_hours))
    user_count_last_24_hours = result_last_24_hours[0]["user_count_last_24_hours"] if result_last_24_hours else 0
    user_count_previous_24_hours = result_previous_24_hours[0]["user_count_previous_24_hours"] if result_previous_24_hours else 0
    user_count_difference = user_count_last_24_hours - user_count_previous_24_hours
    print("Visitor Count Last 24 Hours:", user_count_last_24_hours)
    print("Visitor Count Difference 24 Hours:", user_count_difference)



def total_visit_last_7_days():
    current_utc_time = datetime.utcnow()
    start_time_last_7_days = current_utc_time - timedelta(days=7)
    start_time_previous_7_days = start_time_last_7_days - timedelta(days=7)
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
    result_last_7_days = list(collection.aggregate(pipeline_last_7_days))
    result_previous_7_days = list(collection.aggregate(pipeline_previous_7_days))

    user_count_last_7_days = result_last_7_days[0]["user_count_last_7_days"] if result_last_7_days else 0

    user_count_previous_7_days = result_previous_7_days[0]["user_count_previous_7_days"] if result_previous_7_days else 0

    print("Visitor Count Last 7 Days:", user_count_last_7_days)
    print("Visitor Count Previous 7 Days:", user_count_previous_7_days)








# Calculate the start time for the current day


def today_male_female_kids_count_per_day():
    current_utc_time = datetime.utcnow()
    start_time_current_day = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
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

    result_current_day = list(collection.aggregate(pipeline_current_day))
    total_male_current_day = result_current_day[0]["total_male_current_day"] if result_current_day else 0
    total_female_current_day = result_current_day[0]["total_female_current_day"] if result_current_day else 0
    total_kids_current_day = result_current_day[0]["total_kids_current_day"] if result_current_day else 0

    print("Total Male on Current Day:", total_male_current_day)
    print("Total Female on Current Day:", total_female_current_day)
    print("Total Kids on Current Day:", total_kids_current_day)






def avg_hourly_visits():
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






def avg_daily_visit():
    

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

    result_avg_daily_visitors = list(collection.aggregate(pipeline_avg_daily_visitors))

    average_daily_visitors = [{"day_of_week": entry["_id"], "average_visitors": entry["average_daily_visitors"]} for entry in result_avg_daily_visitors]

    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    average_daily_visitors_mapped = [{day_names[entry["day_of_week"] - 1]: entry["average_visitors"]} for entry in average_daily_visitors]

    # Create a JSON response
    json_response = {
        "average_daily_visitors": average_daily_visitors_mapped
    }

    print(json_response)








# ****** NUMBER OF VISITORS FOR LAST 12 MONTHS ********
current_utc_time = datetime.utcnow()
start_time_last_12_months = current_utc_time - timedelta(days=365)


def total_visits_in_last_12_months():
    pass

# Aggregation pipeline for the last 12 months
pipeline_last_12_months = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_12_months, "$lt": current_utc_time}
        }
    },
    {
        "$group": {
            "_id": {
                "year": {"$year": "$TimeStamp"},
                "month": {"$month": "$TimeStamp"}
            },
            "total_visitors": {"$sum": "$NoOfPeople"}
        }
    },
    {
        "$sort": {"_id.year": 1, "_id.month": 1}
    }
]

# Execute the aggregation
result_last_12_months = list(collection.aggregate(pipeline_last_12_months))

# Extract the results
total_visitors_last_12_months = [{"year": entry["_id"]["year"], "month": entry["_id"]["month"], "total_visitors": entry["total_visitors"]} for entry in result_last_12_months]

# Create a JSON response
json_response = {
    "total_visitors_last_12_months": total_visitors_last_12_months
}

# Print the JSON response
ic("****** NUMBER OF VISITORS FOR LAST 12 MONTHS ********")
print(json_response)









#******** DAILY VISIT TREND BY GENDER ********************


current_utc_time = datetime.utcnow()

# Calculate the start time for the last 30 days
start_time_last_30_days = current_utc_time - timedelta(days=30)

# Aggregation pipeline for the last 30 days
def today_visit_by_gender_last_30_days():
    pass

pipeline_last_30_days = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_30_days, "$lt": current_utc_time}
        }
    },
    {
        "$group": {
            "_id": {
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$TimeStamp"}},
            },
            "total_male": {"$sum": "$TotalMale"},
            "total_female": {"$sum": "$TotalFemale"}
        }
    },
    {
        "$sort": {"_id.date": 1}
    }
]

# Execute the aggregation
result_last_30_days = list(collection.aggregate(pipeline_last_30_days))

# Extract the results
daily_visit_trend = [{"date": entry["_id"]["date"], "total_male": entry["total_male"], "total_female": entry["total_female"]} for entry in result_last_30_days]

# Create a JSON response
json_response = {
    "daily_visit_trend_last_30_days": daily_visit_trend
}

# Print the JSON response
ic("******** DAILY VISIT TREND BY GENDER ********************")
print(json_response)








# *********** Gender Distribution for last 7 hours *************** 
current_utc_time = datetime.utcnow()

# Calculate the start time for the last 7 hours
start_time_last_7_hours = current_utc_time - timedelta(hours=7)
def today_visit_by_gender_last_7_hours():
    pass
# Aggregation pipeline for the last 7 hours by timeslot
pipeline_last_7_hours = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_7_hours, "$lt": current_utc_time}
        }
    },
    {
        "$project": {
            "hour": {"$hour": "$TimeStamp"},
            "total_male": "$TotalMale",
            "total_female": "$TotalFemale",
            "total_kids": "$TotalKids"
        }
    },
    {
        "$group": {
            "_id": {"hour": "$hour"},
            "total_male": {"$sum": "$total_male"},
            "total_female": {"$sum": "$total_female"},
            "total_kids": {"$sum": "$total_kids"}
        }
    },
    {
        "$sort": {"_id.hour": 1}
    }
]

# Execute the aggregation
result_last_7_hours = list(collection.aggregate(pipeline_last_7_hours))

# Extract the results
gender_distribution_last_7_hours = [
    {
        "hour": entry["_id"]["hour"],
        "total_male": entry["total_male"],
        "total_female": entry["total_female"],
        "total_kids": entry["total_kids"]
    } for entry in result_last_7_hours
]

# Create a JSON response
json_response = {
    "gender_distribution_last_7_hours": gender_distribution_last_7_hours
}

# Print the JSON response
ic("****************** TOTAL MALE AND FEMALE FOR LAST 7 HOURS ****************")
print(json_response)







# ************** Weekly total visitors trends for last 7 weeks ***************
current_utc_time = datetime.utcnow()

# Calculate the start time for the last 7 weeks
start_time_last_7_weeks = current_utc_time - timedelta(weeks=7)

# Aggregation pipeline for the last 7 weeks

def today_visit_in_last_7_weeks():
    pass
pipeline_last_7_weeks = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_7_weeks, "$lt": current_utc_time}
        }
    },
    {
        "$group": {
            "_id": {"$week": "$TimeStamp"},
            "total_visitors": {"$sum": "$NoOfPeople"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

result_last_7_weeks = list(collection.aggregate(pipeline_last_7_weeks))

weekly_visit_trend = [{"week": entry["_id"], "total_visitors": entry["total_visitors"]} for entry in result_last_7_weeks]

json_response = {
    "weekly_visit_trend_last_7_weeks": weekly_visit_trend
}

ic("************** Weekly total visitors trends for last 7 weeks ***************")
print(json_response)








# *********** Weekly visiotrs trend for male and female  ************** 
current_utc_time = datetime.utcnow()

# Calculate the start time for the last 7 weeks
start_time_last_7_weeks = current_utc_time - timedelta(weeks=7)

# Aggregation pipeline for the last 7 weeks by TotalMale and TotalFemale
def today_visit_by_gender_last_7_weeks():
    pass
pipeline_last_7_weeks_gender = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_7_weeks, "$lt": current_utc_time}
        }
    },
    {
        "$project": {
            "week": {"$week": "$TimeStamp"},
            "total_male": "$TotalMale",
            "total_female": "$TotalFemale"
        }
    },
    {
        "$group": {
            "_id": {"week": "$week"},
            "total_male": {"$sum": "$total_male"},
            "total_female": {"$sum": "$total_female"}
        }
    },
    {
        "$sort": {"_id.week": 1}
    }
]

# Execute the aggregation
result_last_7_weeks_gender = list(collection.aggregate(pipeline_last_7_weeks_gender))

# Extract the results
weekly_gender_visit_trend = [
    {
        "week": entry["_id"]["week"],
        "total_male": entry["total_male"],
        "total_female": entry["total_female"]
    } for entry in result_last_7_weeks_gender
]

# Create a JSON response
json_response = {
    "weekly_gender_visit_trend_last_7_weeks": weekly_gender_visit_trend
}

# Print the JSON response
ic("*********** Weekly visiotrs trend for male and female  ************** ")
print(json_response)








# ********* MONTHLY VISITORS TREND FOR MALE AND FEMALE FOR LAST 12 MONTHS **************
current_utc_time = datetime.utcnow()

# Calculate the start time for the last 12 months
start_time_last_12_months = current_utc_time - timedelta(days=365)

# Aggregation pipeline for the last 12 months by TotalMale and TotalFemale
def today_visit_by_gender_last_12_months():
    pass
pipeline_last_12_months_gender = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_12_months, "$lt": current_utc_time}
        }
    },
    {
        "$project": {
            "month": {"$month": "$TimeStamp"},
            "total_male": "$TotalMale",
            "total_female": "$TotalFemale"
        }
    },
    {
        "$group": {
            "_id": {"month": "$month"},
            "total_male": {"$sum": "$total_male"},
            "total_female": {"$sum": "$total_female"}
        }
    },
    {
        "$sort": {"_id.month": 1}
    }
]

# Execute the aggregation
result_last_12_months_gender = list(collection.aggregate(pipeline_last_12_months_gender))

# Extract the results
monthly_gender_visit_trend = [
    {
        "month": entry["_id"]["month"],
        "total_male": entry["total_male"],
        "total_female": entry["total_female"]
    } for entry in result_last_12_months_gender
]

# Create a JSON response
json_response = {
    "monthly_gender_visit_trend_last_12_months": monthly_gender_visit_trend
}

# Print the JSON response
ic("********* MONTHLY VISITORS TREND FOR MALE AND FEMALE FOR LAST 12 MONTHS **************")
print(json_response)