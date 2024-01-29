from pydantic import BaseModel

class TrafficInfo(BaseModel):
    siteID: str
    # totalCapacity: int
    noOfPeople: int
    totalTraffic: int
    totalMale: int
    totalFemale: int
    totalKids: int 

class OrderTime(BaseModel):
    siteID: str
    orderTime: int

class IdolTime(BaseModel):
    siteID: str
    IdolTime: int
    image: str

class QueueTime(BaseModel):
    siteID: int
    queueTime: int
    totalIndividuals: int

class Login(BaseModel):
    username: str
    password: str

class Site(BaseModel):
    user_id: str
    location: str

class Admin(BaseModel):
    pass 
