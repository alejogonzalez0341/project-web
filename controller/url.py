from fastapi import APIRouter, HTTPException, status, Depends,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from admin.oauth2 import get_user_disabled_current

from .crud import get_id, created_product, get_all_products

from admin.oauth2 import oauth2_scheme

from models.schemas import Products
from models.db import engine, session_local, base

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
    return templates.TemplateResponse(request=request, name="login.html")


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
