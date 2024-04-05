from fastapi import FastAPI

from admin.url import admin_router
from controller.url import routers


app= FastAPI()

app.include_router(router=admin_router)
app.include_router(router=routers)