from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from admin.url import admin_router
from controller.url import routers


app= FastAPI()

app.mount('/static', StaticFiles(directory='views/static'), name='static')

app.include_router(router=admin_router)
app.include_router(router=routers)