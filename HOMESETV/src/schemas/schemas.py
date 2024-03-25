from pydantic import BaseModel, EmailStr, StringConstraints, field_validator, model_validator, Field, field_serializer
from pydantic_extra_types import phone_numbers
from typing_extensions import Annotated, Dict, Any, List
from bson import ObjectId


class Login(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(strip_whitespace=False, min_length=8 )]


class Signup(BaseModel):
    model_config = {"arbitrary_types_allowed":True}
    userName : Annotated[str, StringConstraints(strip_whitespace=False, max_length=100, min_length=2)]
    email: EmailStr
    password1: Annotated[str, StringConstraints(strip_whitespace=False, min_length=8 )]
    password2: Annotated[str, StringConstraints(strip_whitespace=False, min_length=8 )]
    termsConditions: bool


    @field_validator("termsConditions",mode="after")
    @classmethod
    def check_termsConditions(cls, v:bool): 
        if v is not True: 
            raise ValueError("terms and conditions should be acknowledged")
        return v
    
    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self

class ProfileRET(BaseModel): 
    model_config = {"arbitrary_types_allowed": True}
    id:  ObjectId = Field(alias="_id", exclude=True)
    email: EmailStr
    userName:str
    roles: List[str]
    plan: None | str

    @field_serializer('id', return_type=str)
    def serialize_courses_in_order(id: ObjectId):
        return str(id)
    
class Password(BaseModel): 
    currentPassword: str
    newPassword: str
    