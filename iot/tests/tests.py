
def test_total_visit_last_7_days(collection):
    current_utc_time = datetime.utcnow()
    start_time_last_7_days = current_utc_time - timedelta(days=7)
    start_time_previous_7_days = start_time_last_7_days - timedelta(days=7) 
    records = collection.find({"TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}})
    tt = 0
    tt_2 = 0
    count = 0
    for re in records: 
        count+=1
        tt += re["Totaltrafic"]
        if re["Totaltrafic"] > 100: 
            tt_2 += re["Totaltrafic"]
    ic (tt)
    ic(tt_2)
    ic(count)




def test_hourly_visits_last_24h(collection): 
    current_utc_time = datetime.utcnow()
    start_time_last_7_days = current_utc_time - timedelta(hours=24)
    records = collection.find({"TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}})
    tt = 0
    # tt_2 = 0
    count = 0
    for re in records: 
        count+=1
        tt += re["Totaltrafic"]
        # if re["Totaltrafic"] > 100: 
        #     tt_2 += re["Totaltrafic"]
    ic (tt)
    # ic(tt_2)
    ic(count)




# def test2_calculate_daily_visits_for_last_7d(collection): 
#     start_time_last_7_days = datetime.utcnow() - timedelta(days=7)

# # Initialize a dictionary to store total traffic for each day
#     total_traffic_per_day = {}

#     # Query for records within the last 7 days
#     records = collection.find({"TimeStamp": {"$gte": start_time_last_7_days}})

#     # Calculate total traffic for each day
#     for record in records:
#         # Extract the date without hours, minutes, and seconds
#         date_key = record["TimeStamp"].replace(hour=0, minute=0, second=0, microsecond=0)
        
#         # Update the total traffic for the day
#         total_traffic_per_day[date_key] = total_traffic_per_day.get(date_key, 0) + record["Totaltrafic"]

#     # Print the result
#     for date, total_traffic in total_traffic_per_day.items():
#         print(f"Date: {date}, Total Traffic: {total_traffic}")

def test_calculate_daily_visits_for_last_7d(collection): 
    current_utc_time = datetime.utcnow()
    start_time_last_7_days = current_utc_time - timedelta(days=7)
    records = collection.find({"TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}})
    tt = 0
    for re in records: 
        tt += re["Totaltrafic"]
    ic (tt)







def test_busiest_hour_7_days(collection): 
    current_utc_time = datetime.utcnow()
    start_time_last_7_days = current_utc_time - timedelta(hours=24)
    records = collection.find({"TimeStamp": {"$gte": start_time_last_7_days, "$lt": current_utc_time}})
    tt = 0
    for re in records: 
        tt += re["Totaltrafic"]
    ic (tt)