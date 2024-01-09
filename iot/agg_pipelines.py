from datetime import datetime, timedelta
from pymongo import MongoClient
from icecream import ic

# Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["CoffeeShop"]
# cd = db["Data"]
def total_visit_last_24_hours(collection):
    current_utc_time = datetime.utcnow()
    start_time_last_24_hours = current_utc_time - timedelta(hours=24)
    start_time_previous_24_hours = start_time_last_24_hours - timedelta(hours=24)
        
    pipeline_last_24_hours = [
        
        {
            "$match": {
                "TimeStamp": {"$gte": start_time_last_24_hours, "$lt": current_utc_time}
            }
        },
        {
            "$group": {
                "_id": None,
                "user_count_last_24_hours": {"$sum": "$Totaltrafic"}
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
                "user_count_previous_24_hours": {"$sum": "$Totaltrafic"}
            }
        }
    ]

    result_last_24_hours = list(collection.aggregate(pipeline_last_24_hours))
    result_previous_24_hours = list(collection.aggregate(pipeline_previous_24_hours))

    
    user_count_last_24_hours = result_last_24_hours[0]["user_count_last_24_hours"] if result_last_24_hours else 0
    user_count_previous_24_hours = result_previous_24_hours[0]["user_count_previous_24_hours"] if result_previous_24_hours else 0
    user_count_difference = user_count_last_24_hours - user_count_previous_24_hours
    print("Visitor Count Last 24 Hours:", user_count_last_24_hours)
    print("Visitor Count Difference 24 Hours:", user_count_previous_24_hours)
    json_response = {
        "visitorLast24Hour":user_count_last_24_hours,
        "visitorPrevious24Hour": user_count_previous_24_hours
    }
    return json_response








def total_visit_last_7_days(collection):
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
                "user_count_last_7_days": {"$sum": "$Totaltrafic"}
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
                "user_count_previous_7_days": {"$sum": "$Totaltrafic"}
            }
        }
    ]
    result_last_7_days = list(collection.aggregate(pipeline_last_7_days))
    result_previous_7_days = list(collection.aggregate(pipeline_previous_7_days))

    user_count_last_7_days = result_last_7_days[0]["user_count_last_7_days"] if result_last_7_days else 0

    user_count_previous_7_days = result_previous_7_days[0]["user_count_previous_7_days"] if result_previous_7_days else 0

    print("Visitor Count Last 7 Days:", user_count_last_7_days)
    print("Visitor Count Previous 7 Days:", user_count_previous_7_days)
    json_response = {
        "visitorLast7Days":user_count_last_7_days, 
        "visitorPrevious7Days": user_count_previous_7_days
    }

    return json_response










def total_male_female_kids_count_24h7d30d(collection):
    current_utc_time = datetime.utcnow()
    # Calculate the start time for the last 24 hours
    start_time_last_24_hours = current_utc_time - timedelta(hours=24)

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
                "total_male": {"$sum": "$TotalMale"},
                "total_female": {"$sum": "$TotalFemale"},
                "total_kids": {"$sum": "$TotalKids"}
            }
        }
    ]

    # Execute the aggregation
    result_last_24_hours = list(collection.aggregate(pipeline_last_24_hours))

    # Print the result
    ic(result_last_24_hours)




    # Calculate the start time for the last 7 days
    start_time_last_7_days = current_utc_time - timedelta(days=7)

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
                "total_male": {"$sum": "$TotalMale"},
                "total_female": {"$sum": "$TotalFemale"},
                "total_kids": {"$sum": "$TotalKids"}
            }
        }
    ]

    # Execute the aggregation
    result_last_7_days = list(collection.aggregate(pipeline_last_7_days))

    # Print the result
    ic(result_last_7_days)




    # Calculate the start time for the last 30 days
    start_time_last_30_days = current_utc_time - timedelta(days=30)

    # Aggregation pipeline for the last 30 days
    pipeline_last_30_days = [
        {
            "$match": {
                "TimeStamp": {"$gte": start_time_last_30_days, "$lt": current_utc_time}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_male": {"$sum": "$TotalMale"},
                "total_female": {"$sum": "$TotalFemale"},
                "total_kids": {"$sum": "$TotalKids"}
            }
        }
    ]

    # Execute the aggregation
    result_last_30_days = list(collection.aggregate(pipeline_last_30_days))

    # Print the result
    ic(result_last_30_days)
    if len(result_last_7_days) > 0:
        result_last_7_days[0].pop("_id")
    if len(result_last_24_hours) > 0:
        result_last_24_hours[0].pop("_id")
    if len(result_last_30_days) > 0:
        result_last_30_days[0].pop("_id")

    # print("____________________-")
    result = {"total_m_f_k_24h": result_last_24_hours[0] if len(result_last_24_hours) >0 else [], 
              "total_m_f_k_7d": result_last_7_days[0] if len(result_last_7_days) >0 else [], 
              "total_m_f_k_30d": result_last_30_days[0] if len(result_last_30_days) >0 else []}
    print(result)
    return result












# * _______________________ API 2 ___________________________


def hourly_visits_last_24h(collection):
    end_time = datetime.utcnow()
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
                    "total_traffic": {"$sum": "$Totaltrafic"}
                }
            },
            {
                "$sort": {"_id.hour": 1}
            }
        ]


    # Execute the aggregation pipeline

    # Format the result into JSON
    result_hourly_visits = list(collection.aggregate(pipeline_hourly_visits))
    # print(result_hourly_visits)
    formatted_result = [{"hour": entry["_id"]["hour"], "total_traffic": entry["total_traffic"]} for entry in result_hourly_visits]

    json_response = {"hourlyVisits": formatted_result}
    # ic(json_response)
    # result = {"hourlyVisits": []}
    for visit in json_response["hourlyVisits"]:
        visit['hour'] = (visit['hour'] + 3) % 24

    ic(json_response)
    # ic(result)
    return json_response















def calculate_daily_visits_for_last_7d(collection):
    current_utc_time = datetime.utcnow()

    start_time_last_7_days = current_utc_time - timedelta(days=7)

    pipeline_daily_visits_last_7_days = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_7_days}
        }
    },
    {
        "$group": {
            "_id": {
                "$dateToString": {"format": "%Y-%m-%d", "date": "$TimeStamp"}
            },
            "total_visits": {"$sum": "$Totaltrafic"}
        }
    },
    {
        "$sort": {"_id": 1}
    },
    {
        "$project": {
            "_id": 0,
            "date": "$_id",
            "total_visits": 1
        }
    }
    ]
    

    json_result = list(collection.aggregate(pipeline_daily_visits_last_7_days))
    json_result = {"daily_visits_7_days": json_result}
    ic(json_result)
    return json_result











def busiest_hour_7_days(collection):
    start_time_last_7_days = datetime.utcnow() - timedelta(days=7)

# Aggregation pipeline
    pipeline = [
    {
        "$match": {
            "TimeStamp": {"$gte": start_time_last_7_days}
        }
    },
    {
        "$addFields": {
            "hour": {"$hour": {"date": "$TimeStamp", "timezone": "+00:00"}}
        }
    },
    {
        "$group": {
            "_id": {
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$TimeStamp", "timezone": "+00:00"}},
                "hour": "$hour"
            },
            "visits": {"$sum": "$Totaltrafic"}
        }
    },
    {
        "$group": {
            "_id": "$_id.date",
            "hourlyVisits": {
                "$push": {
                    "hour": "$_id.hour",
                    "visits": "$visits"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "date": "$_id",
            "hourlyVisits": 1
        }
    },
    {
        "$sort": {
            "date": 1
        }
    },
    {
        "$group": {
            "_id": None,
            "result": {
                "$push": {
                    "k": "$date",
                    "v": "$hourlyVisits"
                }
            }
        }
    },
    {
        "$replaceRoot": {
            "newRoot": {
                "$arrayToObject": "$result"
            }
        }
    }
]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))
    # ic (result)
    for date_visits in result:
        for date, hourly_visits in date_visits.items():
            sorted_hourly_visits = sorted(hourly_visits, key=lambda x: x['hour'])

            date_visits[date] = sorted_hourly_visits
    
    sa_hour_convertion = {}
    if len(result) > 0:
        for key,value in result[0].items(): 
            sa_hour_convertion.update({key:[]})
            
            for hour_visit_dict in value:
                modified_hour = {}
                modified_hour.update({"hour": (hour_visit_dict['hour'] + 3) % 24, "visits":hour_visit_dict["visits"]})
                sa_hour_convertion[key].append(modified_hour)
        result = {"busiestHour7Days": sa_hour_convertion}
        ic(result)
        return result
    
    result = {"busiestHour7Days": None}
    return result







# * _________________________________ API 3 ________________________________

def gender_trend_30_days(collection):
    current_utc_time = datetime.utcnow()
    start_time_last_30_days = current_utc_time - timedelta(days=30)
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
                "total_female": {"$sum": "$TotalFemale"},
                "total_kids": {"$sum": "$TotalKids"}
            }
        },
        {
            "$sort": {"_id.date": 1}
        }
    ]

    # Execute the aggregation
    result_last_30_days = list(collection.aggregate(pipeline_last_30_days))

    # Extract the results
    daily_visit_trend = [{"date": entry["_id"]["date"], "total_male": entry["total_male"], "total_female": entry["total_female"],"total_kids": entry["total_kids"] } for entry in result_last_30_days]

    # Create a JSON response
    json_response = {
        "genderTrend30Days": daily_visit_trend
    }

    # Print the JSON response
    ic("******** DAILY VISIT TREND BY GENDER ********************")
    print(json_response)
    return json_response







def gender_trend_last_7_weeks(collection):
    current_utc_time = datetime.utcnow()
    start_time_last_7_weeks = current_utc_time - timedelta(weeks=7)
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
                "total_female": "$TotalFemale",
                "total_kids": "$TotalKids",
            }
        },
        {
            "$group": {
                "_id": {"week": "$week"},
                "total_male": {"$sum": "$total_male"},
                "total_female": {"$sum": "$total_female"},
                "total_kids": {"$sum": "$total_kids"},
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
            "total_female": entry["total_female"],
            "total_kids": entry["total_kids"],

        } for entry in result_last_7_weeks_gender
    ]

    # Create a JSON response
    json_response = {
        "genderTrendLast7Weeks": weekly_gender_visit_trend
    }

    # Print the JSON response
    ic("*********** Weekly visiotrs trend for male and female  ************** ")
    print(json_response)
    return json_response











def gender_trend_12_months(collection):
    current_utc_time = datetime.utcnow()
    # Calculate the start time for the last 12 months
    start_time_last_12_months = current_utc_time - timedelta(days=365)
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
                "total_female": "$TotalFemale",
                "total_kids": "$TotalKids",
            }
        },
        {
            "$group": {
                "_id": {"month": "$month"},
                "total_male": {"$sum": "$total_male"},
                "total_female": {"$sum": "$total_female"},
                "total_kids": {"$sum": "$total_kids"},
            }
        },
        {
            "$sort": {"_id.month": 1}
        }
    ]

    # Execute the aggregation
    result_last_12_months_gender = list(collection.aggregate(pipeline_last_12_months_gender))
    # ic(result_last_12_months_gender)
    # Extract the results
    monthly_gender_visit_trend = [
        {
            "month": entry["_id"]["month"],
            "total_male": entry["total_male"],
            "total_female": entry["total_female"],
            "total_kids": entry["total_kids"],
        } for entry in result_last_12_months_gender
    ]

    # Create a JSON response
    json_response = {
        "genderTrendLast12Months": monthly_gender_visit_trend
    }

    # Print the JSON response
    ic("********* MONTHLY VISITORS TREND FOR MALE AND FEMALE FOR LAST 12 MONTHS **************")
    print(json_response)
    return json_response








# * ______________________________ API 4 ___________________________________




def monthly_visitors_count(collection):
    current_utc_time = datetime.utcnow()
    start_time_last_12_months = current_utc_time - timedelta(days=365)
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
                "total_visitors": {"$sum": "$Totaltrafic"}
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
        "totalVisitsLast12Months": total_visitors_last_12_months
    }

    # Print the JSON response
    # ic("****** NUMBER OF VISITORS FOR LAST 12 MONTHS ********")
    # print(json_response)
    return json_response








def gender_trend_last_7_hours(collection):
    current_utc_time = datetime.utcnow()
    start_time_last_7_hours = current_utc_time - timedelta(hours=7)
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
        "genderTrendLast7Hours": gender_distribution_last_7_hours
    }

    sa_hour_convertion = {"genderTrendLast7Hours": []}
    # ic(json_response)
    for i in json_response["genderTrendLast7Hours"]:
        # ic(i)
        temp = {}
        temp.update({"hour": (i['hour'] + 3) % 24, "total_male":i["total_male"], 
                     "total_female": i["total_female"], "total_kids": i["total_kids"]})
        sa_hour_convertion["genderTrendLast7Hours"].append(temp)


    ic(sa_hour_convertion)
    return sa_hour_convertion