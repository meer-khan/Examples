from pydantic import BaseModel, EmailStr

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

class AdminLogin(BaseModel):
    username: str
    password: str

class SiteRegistration(BaseModel):
    adminId: str
    email: EmailStr
    location: str
    totalCapacity:int
    longitude: float
    latitude: float

class SiteLogin(BaseModel):
    email: str
    password: str


class Admin(BaseModel):
    pass 
