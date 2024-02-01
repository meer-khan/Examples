from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from icecream import ic
from decouple import config

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    ic(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
        ic(payload)
        email: str = payload.get("email")
        id :str = payload.get("id")

        if email is None or id is None: 
            return credentials_exception
        # ic(id)
        token_data = schemas.TokenData(email=email, id= id)

    except JWTError: 
        return credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception =  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail = "Unauthorized user",
        headers={"WWW.Authenticate": "Bearer"})
    
    return verify_token(token, credentials_exception)