from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer, field_validator, PlainSerializer
from fastapi import UploadFile
from bson import ObjectId
from icecream import ic
from typing_extensions import Annotated, Dict, Any


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

# class ObjectIdStr(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v) -> str:
#         if not isinstance(v, ObjectId):
#             raise ValueError('Not a valid ObjectId')
#         return str(v)

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

class AdminRegistration(BaseModel): 
    email: EmailStr



class AdminRegistrationReturn(BaseModel): 
    id: str
    email: EmailStr
    password: str


# try:
class AdminProfile(BaseModel): 
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id : str = Field(alias="_id", strict=False)
    email:str

    # @field_serializer('_id', when_used='always', check_fields=False)
    # def serialize_id_to_str(_id: str):
    #     return _id

class SAAdminSitesRet(BaseModel): 

    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id : str = Field(alias="_id", title="Document Id")
    email: EmailStr
    name: str
    location: str
    totalCapacity: int 
    cordinates: dict
    active_status: bool
    show_data: bool
    # @field_serializer("_id", return_type=str , check_fields=False)
    # def type_converter(_id: ObjectId ): 
    #     return str(_id)
    # @field_validator('_id', mode="before",  check_fields=False)
    # @classmethod
    # def change_type(cls, v: ObjectId):
    #     ic(v)
    #     print("HELLO MY FIREND")
    #     return str(v)




class TokenData(BaseModel):
    email: EmailStr
    id: str



class QueueTime(BaseModel):
    siteId:str 
    queueTime: int
    totalIndividuals: int


class IdolTime(BaseModel):
    siteId:str 
    image: bytes
    idolTime: int

class IdolTime(BaseModel):
    siteId:str 
    image: bytes
    idolTime: int

class OrderTime(BaseModel): 
    siteId: str
    orderTime: int


class TrafficInfo(BaseModel):
    siteId: str
    noOfPeople: int
    totalTraffic: int
    totalMale: int
    totalFemale: int
    totalKids: int 