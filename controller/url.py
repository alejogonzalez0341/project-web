from fastapi import APIRouter, HTTPException, status, Depends, Request, Cookie
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from typing import Annotated
from jose import JWTError, jwt
from dotenv import dotenv_values

from admin.oauth2 import get_user_disabled_current, get_user

from .crud import get_id, created_product, get_all_products

from admin.oauth2 import oauth2_scheme
from admin.db import admin_user_db

from models.schemas import Products
from models.db import engine, session_local, base

config_env= dotenv_values(".env")

SECRET_KEY= config_env["SECRET_KEY"]
ALHORITHM= config_env["ALGORITHM"]

routers= APIRouter()

templates= Jinja2Templates(directory="views/templates")

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


@routers.get("/admin", response_class=HTMLResponse)
def admin(request:Request, access_token: Annotated[ str | None, Cookie()]= None):
    if access_token is None:
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    try:
        data_user= jwt.decode(access_token, key=SECRET_KEY, algorithms=ALHORITHM)
        if get_user(admin_user_db, data_user["sub"]) is None:
            return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    except JWTError:
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="admin.html")



@routers.post("/newproduct", response_model=Products, dependencies=[Depends(oauth2_scheme)], tags=["Products"], status_code=status.HTTP_201_CREATED)
def new_products(product_: Products, db:Session= Depends(get_db)):
    id_product= get_id(db=db, id=product_.id)
    if id_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id already registered"
        )
    return created_product(db=db, products=product_)



@routers.get("/products", response_model=list[Products], tags=["Products"], status_code=status.HTTP_200_OK)
def get_products(skip:int=0, limit:int=100,db: Session = Depends(get_db)):
    return  get_all_products(db=db, skip=skip, limit=limit)
