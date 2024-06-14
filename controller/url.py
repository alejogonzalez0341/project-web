from fastapi import APIRouter, HTTPException, status, Depends, Request, Cookie,UploadFile, File
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import uuid

from typing import Annotated
from jose import JWTError, jwt
from dotenv import dotenv_values

from admin.oauth2 import get_user_disabled_current, get_user

from .crud import get_id, created_product, get_all_products, update_product

from admin.oauth2 import oauth2_scheme
from admin.db import admin_user_db

from models.schemas import GetProduct, ProductsCreate
from models.db import engine, session_local, base

config_env= dotenv_values(".env")

SECRET_KEY= config_env["SECRET_KEY"]
ALHORITHM= config_env["ALGORITHM"]

routers= APIRouter()

templates= Jinja2Templates(directory="views/templates")

IMAGESDIR= "view/static/images/"


base.metadata.create_all(bind=engine)


def get_db():
    db= session_local()
    try:
        yield db
    finally:
        db.close()


@routers.get("/", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(request=request, name="index.html")

@routers.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


# @routers.get("/admin", response_class=HTMLResponse)
# def admin(request:Request, access_token: Annotated[ str | None, Cookie()]= None):
#     if access_token is None:
#         return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
#     try:
#         data_user= jwt.decode(access_token, key=SECRET_KEY, algorithms=ALHORITHM)
#         if get_user(admin_user_db, data_user["sub"]) is None:
#             return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
#     except JWTError:
#         return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
#     return templates.TemplateResponse(request=request, name="admin/index.html")


@routers.get("/products", response_model=list[ProductsCreate], tags=["Products"], status_code=status.HTTP_200_OK)
def get_products(skip:int=0, limit:int=100,db: Session = Depends(get_db)):
    return  get_all_products(db=db, skip=skip, limit=limit)


@routers.post("/newproduct", response_model=GetProduct, dependencies=[Depends(oauth2_scheme)], tags=["Products"], status_code=status.HTTP_201_CREATED)
def new_products(product_: ProductsCreate, db:Session= Depends(get_db)):
    id_product= get_id(db=db, id=product_.id)
    
    if id_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id already registered"
        )
        
    return created_product(db=db, products=product_)



@routers.put("/update_product{id_product}")
def update(id_product:int, product_:ProductsCreate, db:Session = Depends(get_db)):
    return update_product(db=db, id=id_product, product=product_)