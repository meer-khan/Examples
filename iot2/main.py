from fastapi import FastAPI
from routers import data_routes

app = FastAPI()

app.include_router(data_routes.router)