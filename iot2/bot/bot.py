'''
Bot is deigned to do query performance testing after insterting data into database
'''
from icecream import ic
import db
import dbquery
import random
import time

def random_generator(start , end): 
    num = random.randint(a=start, b=end)
    return num


def generate_traffic(start, end):
    # Generate random values for total_traffic
    total_traffic = random_generator(start,end)

    # Randomly divide total_traffic into three subsets
    total_male = random_generator(0, total_traffic)
    total_female = random_generator(0, total_traffic - total_male)
    total_kids = total_traffic - total_male - total_female

    return total_traffic , total_male, total_female, total_kids


def insert_data(): 
    for i in range (10000): 
        time.sleep(3)
        total_traffic , total_male, total_female, total_kids = generate_traffic(0, 10)
        ic(total_traffic)
        ic(total_male)
        ic(total_female)
        ic(total_kids)
        ic("*******************")
        dbquery.add_data( cd,
                        site_id="65bbf817b9834d683b160224",
                        no_of_people= random_generator(0,10), 
                        total_traffic=total_traffic, 
                        total_male=total_male,
                        total_female=total_female,
                        total_kids=total_kids)

if __name__ == "__main__": 
    csa, ca, cs, cd, cqst, ccit, ccot = db.main()
    insert_data()