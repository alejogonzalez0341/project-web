from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from datetime import timedelta

from dotenv import dotenv_values

#importaciones del mismo modulo
from .oauth2 import authenticate_user, create_token
from .db import admin_user_db
from .schemes import Token

#importaciones de otros modulos
from controller.crud import new_register_banner, get_all_banners, get_id_banner, update_banner, delete_banner
from controller.url import get_db

from models.schemas import BannerProductRequest, ResponseBanner
from models.models import MBanner, MPorducts

templates= Jinja2Templates(directory="views/templates/admin")

config_env= dotenv_values(".env")

TOKEN_SCONDS_EXP= config_env["TOKEN_SCONDS_EXP"]

admin_router= APIRouter()

# ruta la cual hace la autenticación del usuario
@admin_router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user= authenticate_user(admin_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username o password incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires= timedelta(seconds=10)
    access_token_jwt=  create_token(data={"sub": user.username}, time_expire=access_token_expires)
    """ return RedirectResponse("admin",
                            status_code=status.HTTP_302_FOUND,
                            headers={"set-cookie": f"access_token={access_token_jwt}; Max-Age={TOKEN_SCONDS_EXP}"}
                            )"""
    return Token(access_token=access_token_jwt, token_type="Bearer")


####################################### Rutas GET #######################################

#ruta get inicial
@admin_router.get("/admin", response_class=HTMLResponse)
def index_admin(request:Request):
    return templates.TemplateResponse(request=request, name="index.html")

        ############################ Banners #############################

#ruta get banner inicial
@admin_router.get("/admin/banner", response_class=HTMLResponse)
def index_admin(request:Request, db:Session = Depends(get_db)):
    context = {"context":get_all_banners(db=db, skip=0, limit=100)}
    return templates.TemplateResponse(request=request, name="banner/index.html", context=context)


#ruta para crear un registro del banner
@admin_router.get("/admin/banner/crear", response_class=HTMLResponse)
def banner_crear_get(request: Request):
    return templates.TemplateResponse(request=request, name="banner/crear.html")

#ruta para editar registro del banner
@admin_router.get("/admin/banner/editar/{id}", response_class=HTMLResponse)
def banner_edit_get(id: int, request: Request, db:Session = Depends(get_db)):
    #almacenamos los valores de la funcion el una variable
    result_fun= get_id_banner(db=db, id=id)
    #validamos si nos retorna algun dato
    if result_fun is None:
        #damos un error al usuario si la respuesta de la función es vacia 
        raise HTTPException(status_code=404, detail="Elemento del banner no encontrado")
    #definimos el json context en una variable para enviar los datos de la función al html
    context = {"context": result_fun}
    #retornamos un html en la url
    return templates.TemplateResponse(request=request, name="banner/editar.html", context=context)

#ruta para elinimar un dato del banner
@admin_router.get("/admin/banner/delete/{id}", response_class=HTMLResponse)
def delete_banner_delete(id: int, db: Session = Depends(get_db)):
    #validamos que no sea vacia la respuesta
    if delete_banner(db=db, id=id) is False:
        #si es vacia le damos un error al usuario
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo eliminar el elemento porque no se encontró")
    #redireccionamos despues de eliminar el registro del banner a la plantilla html inicial del banner
    return RedirectResponse(url="/admin/banner/", status_code=status.HTTP_303_SEE_OTHER)

        ############################ Catalogo #############################

#ruta get catálogo
@admin_router.get("/admin/catalogo", response_class=HTMLResponse)
def index_admin(request:Request):
    return templates.TemplateResponse(request=request, name="catalogo/index.html")

############################ Nosotros #############################

#ruta get nosotros inicial
@admin_router.get("/admin/nosotros", response_class=HTMLResponse)
def index_admin(request:Request):
    return templates.TemplateResponse(request=request, name="nosotros/index.html")

#ruta crear un registro nosotros
@admin_router.get("/admin/nosotros/crear", response_class=HTMLResponse)
def nosotros_crear_get(request: Request):
    return templates.TemplateResponse(request=request, name="nosotros/crear.html")


####################################### Rutas POST #######################################

        ############################ Banners #############################

#ruta para crear resivir los datos de creacion para el banner
@admin_router.post("/admin/banner/create", response_class=HTMLResponse)
def create_banner_post(title=Form(...), description=Form(...), db: Session = Depends(get_db)):
    #guardamos los datos que resivimos por el form y los igualamos al schema  BannerProductRequest para poder mandarla a la función
    data = BannerProductRequest(title=title, description=description)
    #validamos de que la función no este vacia
    if new_register_banner(db=db, data=data) is False:
        #si es vacia le damos un error al usuario
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no se pudo hacer")
    #redireccionamos despues de crear el nuevo registro del banner a la plantilla html inicial del banner
    return RedirectResponse(url="/admin/banner/", status_code=status.HTTP_303_SEE_OTHER)

#ruta para actualizar un dato del banner mediante un id 
@admin_router.post("/admin/banner/update/{id}", response_class=HTMLResponse)
def update_banner_put(id: int, title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    #guardamos los datos resividos en el schema para mandarlo ala función 
    data = BannerProductRequest(title=title, description=description)
    #validamos que no sea vacia la respuesta
    if update_banner(db=db, id=id, data=data) is None:
        #si es vacia le damos un error al usuario
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No se pudo actualizar el elemento porque no se encontró")
    #redireccionamos despues de actualizar el registro del banner a la plantilla html inicial del banner
    return RedirectResponse(url="/admin/banner/", status_code=status.HTTP_303_SEE_OTHER)
        
        ############################ Nosotros #############################
        
