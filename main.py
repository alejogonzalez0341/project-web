from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import admin.url as admin_url
import controller.url as controller_url


app= FastAPI()

app.mount('/static', StaticFiles(directory='views/static'), name='static')

app.include_router(router=admin_url.admin_router)
app.include_router(router=controller_url.routers)