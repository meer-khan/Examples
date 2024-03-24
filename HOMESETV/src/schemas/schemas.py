from pydantic import BaseModel, EmailStr, StringConstraints, field_validator, model_validator, Field, field_serializer
from pydantic_extra_types import phone_numbers
from typing_extensions import Annotated, Dict, Any, List

class Login(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(strip_whitespace=False, min_length=8 )]


class Signup(BaseModel):
    model_config = {"arbitrary_types_allowed":True}
    firstName : Annotated[str, StringConstraints(strip_whitespace=False, max_length=25, min_length=2)]
    lastName : Annotated[str, StringConstraints(strip_whitespace=False, max_length=25, min_length=2 )]
    email: EmailStr
    password1: Annotated[str, StringConstraints(strip_whitespace=False, min_length=8 )]
    password2: Annotated[str, StringConstraints(strip_whitespace=False, min_length=8 )]
    phoneNo: phone_numbers
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
    id: str = Field(alias="_id")
    email: EmailStr
    firstName: str
    lastName: str
    phoneNo: str
    roles: List[str]
    plan: None | str

    

    # '_id': ObjectId('65fdf3e0ebbe8495813aa115'),
    #          'email': 'shahmirkhan520@gmail.com',
    #          'firstName': 'Shahmeer Khan',
    #          'lastName': 'Khan',
    #          'password': '$2b$12$Uf8tXw2PhCV2rcpglq4Wru7PDPQB616eUrWVSRjHAA0pZgYQiqPeK',
    #          'phoneNo': '0985',
    #          'plan': None,
    #          'roles': ['user'],
    #          'termsConditions': True