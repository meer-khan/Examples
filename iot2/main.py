from fastapi import FastAPI
from fastapi.security.oauth2 import OAuth2PasswordBearer

from routers import data_routes, site_routes, agg_routes, admin_routes, super_admin_routes
import db 

app = FastAPI()
csa, ca, cs, cd, cqst, ccit, ccot = db.main()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(data_routes.router)
app.include_router(site_routes.router)
app.include_router(agg_routes.router)
app.include_router(admin_routes.router)