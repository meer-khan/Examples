from passlib.context import CryptContext
import secrets
import string


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str) -> str:
    return pwd_context.hash(password)


def verify(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password