import pandas as pd
from pymongo import MongoClient



df = pd.read_csv("result_new.csv")

male = df["TotalMale"].sum()

print(male)

