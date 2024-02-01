from pydantic import BaseModel, EmailStr, Field, field_validator, PydanticUserError, ConfigDict
from bson import ObjectId

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
    name: str
    location: str
    totalCapacity:int
    longitude: float
    latitude: float

class Login(BaseModel):
    email: str
    password: str

class GetProfile(BaseModel):
    token:str

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        if not isinstance(v, ObjectId):
            raise ValueError('Not a valid ObjectId')
        return str(v)

class SiteProfile(BaseModel): 
    def __init__(self, **data):
        
        super().__init__(**data)
        print(f"SiteProfile instance created with values: {self.model_dump()}")
        
    _id: ObjectId
    email: EmailStr
    location: str
    name:str
    totalCapacity:int
    cordinates: dict

# try:
class AdminProfile(BaseModel): 
    id : str
    name:str
    location:str

# except PydanticUserError as exc_info:
#     print("*****************")
#     print(exc_info)
#     print("**********************")
#     assert exc_info.code == 'decorator-missing-field'

class TokenData(BaseModel):
    email: EmailStr
    id: str

class Admin(BaseModel):
    pass 
