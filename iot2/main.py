from fastapi import FastAPI
from routers import data_routes, user_routes
import db 

app = FastAPI()
ca, cs, cd, cqst, ccit, ccot = db.main()

app.include_router(data_routes.router)
app.include_router(user_routes.router)