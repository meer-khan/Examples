from pydantic import BaseModel, EmailStr, StringConstraints, field_validator, model_validator
from pydantic_extra_types import phone_numbers
from typing_extensions import Annotated, Dict, Any

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

    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self
