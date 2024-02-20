from datetime import datetime

def add_data(
    cd,
    site_id,
    no_of_people,
    total_traffic,
    total_male,
    total_female,
    total_kids,
):
    cd.insert_one(
        {
            "SiteID": site_id,
            "TimeStamp": datetime.utcnow(),
            "NoOfPeople": no_of_people,
            "Totaltrafic": total_traffic,
            "TotalMale": total_male,
            "TotalFemale": total_female,
            "TotalKids": total_kids,
            "bot": True
        }
    )

def delete_bot_records(collection):

    # Define the filter/query to find records where 'bot' is True
    filter_query = {'bot': True}

    # Delete all records matching the filter
    result = collection.delete_many(filter_query)

    return result.deleted_count  