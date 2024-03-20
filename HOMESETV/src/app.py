from fastapi import FastAPI
from fastapi.security.oauth2 import OAuth2PasswordBearer
# from routers import login_route, signup_route, profile_route
from db.db_connection import db_creation
from routers import signup_route

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
col_user, col_roles, col_plan = db_creation()

# app.include_router(login_route.router)
app.include_router(signup_route.router)
# app.include_router(profile_route.router)
