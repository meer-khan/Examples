import pandas as pd 



# mongodb+srv://<username>:<password>@<cluster-endpoint>/<database-name>?retryWrites=true&w=majority 

# mongodb+srv://mongouser:Admin12345admin@cluster0.pjwv8.mongodb.net/?retryWrites=true&w=majority

# Final output
# mongodb+srv://mongouser:Admin12345admin@<cluster-endpoint>/CoffeeShop?retryWrites=true&w=majority 

path = r"C:\Users\Meer\Downloads\Result_Final_24_Dec.csv"
df = pd.read_csv(path, index_col=False)
df['TimeStamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], utc=True)

# Drop the original 'Date' and 'Time' columns if needed
df = df.drop(['Date', 'Time',"Site-ID", "Customer-ID"], axis=1)

df.rename(columns={"Male Traffic": "TotalMale", "Female Traffic": "TotalFemale", "Children Traffic": "TotalKids", "People Inside": "NoOfPeople", "Daily Traffic": "Totaltrafic"}, inplace=True )
df.to_csv("result_new_24dec.csv")
print(df)