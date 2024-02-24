from datetime import datetime, timedelta
from pymongo import MongoClient
from icecream import ic
import pytz


def db_connection():
    client = MongoClient("mongodb+srv://mongouser:Admin1234Admin@cluster0.pjwv8.mongodb.net/?retryWrites=true&w=majority")
    db = client["CoffeeShop"]
    data = db["Data"]
    return  data





def pipelines(collection):
    #Calculate the timestamp for 7 days ago
    # start_time = datetime.utcnow() - timedelta(days=7)
    sa_tz = pytz.timezone("Asia/Riyadh")
    ct = datetime.now(sa_tz) - timedelta(days=7)
    ic(ct)
    records = collection.find({"TimeStamp": {"$gte": ct}}, {"_id": 0, "DataID": 0, "SiteID": 0, "UserID": 0} )
    # print(records)
    for cur in records:
        print(cur)
        print("________________________________")
        timestamp_utc = cur['TimeStamp']
        ic(type(timestamp_utc))
        timestamp_riyadh = timestamp_utc.astimezone(sa_tz)
        cur['TimeStamp'] = timestamp_riyadh
        print(cur)
        print("*************************************")

def test_busiest_hour_7_days(collection): 
    current_utc_time = datetime.utcnow()
    start_time_last_7_days = current_utc_time - timedelta(hours=24)
    records = collection.find({"TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}})
    tt = 0
    for re in records: 
        tt += re["Totaltrafic"]
    ic (tt)
    # ic(tt_2)
    # ic(count)
 

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
    for key,value in result[0].items():
        sa_hour_convertion.update({key:[]})
        
        for hour_visit_dict in value:
            modified_hour = {}
            modified_hour.update({"hour": (hour_visit_dict['hour'] + 3) % 24, "visits":hour_visit_dict["visits"]})
            sa_hour_convertion[key].append(modified_hour)
    result = {"busiestHour7Days": sa_hour_convertion}
    ic(result)

    return result





if __name__ == "__main__":
    data = db_connection()
    busiest_hour_7_days(data)















# def pipelines(collection): 
    
# # Calculate the timestamp for 7 days ago
#     start_time = datetime.utcnow() - timedelta(days=7)

# # Aggregation pipeline to calculate hourly visits for the last 7 days with Asia/Riyadh timezone
#     pipeline = [
#     {
#         "$match": {
#             "TimeStamp": {"$gte": start_time.isoformat()}
#         }
#     },
#     {
#         "$addFields": {
#             "timestampDate": {
#                 "$dateFromString": {
#                     "dateString": "$TimeStamp",
#                     "format": "%Y-%m-%dT%H:%M:%S.%L",  # Adjust the format based on your timestamp
#                     "timezone": "UTC"
#                 }
#             }
#         }
#     },
#     {
#         "$addFields": {
#             "timestampDate": {
#                 "$dateToParts": {
#                     "date": "$timestampDate",
#                     "timezone": "Asia/Riyadh"
#                 }
#             }
#         }
#     },
#     {
#         "$group": {
#             "_id": None,
#             "hourlyVisits": {
#                 "$push": {
#                     "hour": "$timestampDate.hour",
#                     "totalVisits": "$NoOfPeople"
#                 }
#             }
#         }
#     },
#     {
#         "$sort": {"_id": 1}
#     }
#     ]

#     # Execute the aggregation pipeline
#     result = list(collection.aggregate(pipeline))

#     # Print the result
#     print(result)
