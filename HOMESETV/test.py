

from datetime import timezone 
from icecream import ic
import datetime 
  
  
# Getting the current date 
# and time 
dt_utc = datetime.datetime.now(datetime.UTC)
dt_now = datetime.datetime.now()
# utc_time = dt.replace(tzinfo=timezone.utc) 
# print(utc_time)
# utc_timestamp = utc_time.timestamp() 
  
ic(dt_utc) 
ic(dt_now)