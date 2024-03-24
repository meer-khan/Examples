from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from icecream import ic
from decouple import config

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY_ACCESS = config("SECRET_KEY_ACCESS")
SECRET_KEY_REFRESH = config("SECRET_KEY_REFRESH")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7
REFRESH_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_ACCESS, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY_ACCESS, algorithms=ALGORITHM)
        email: str = payload.get("email")
        id: str = payload.get("id")

        if email is None or id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return email, id


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY_REFRESH, algorithms=ALGORITHM)
        id: str = payload.get("id")

        if id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return id


def get_refresh_token(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized user",
        headers={"WWW.Authenticate": "Bearer"},
    )

    return verify_refresh_token(token, credentials_exception)


def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized user",
        headers={"WWW.Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)
