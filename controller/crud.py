from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.models import MPorducts, MBanner
from models.schemas import ProductsCreate, BannerProductRequest, ResponseBanner

def get_id(db:Session, id:int):
    return db.query(MBanner).filter(MBanner.id == id).first()

def get_all_products(db: Session, skip:int = 0, limit: int = 100):
    return db.query(MPorducts).offset(skip).limit(limit=limit).all()

def created_product(db: Session, products: ProductsCreate):
    product= MPorducts(
        name= products.name,
        type_product= products.type_product,
        descript= products.descript,
        price= products.price
    )
    db.commit()
    db.refresh(product)
    return product


def update_product(db:Session, id:int, product:ProductsCreate):
    product_db=  db.query(MPorducts).filter(MPorducts.id == id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    
    product= MPorducts(
        name= product.name,
        type_product= product.type_product,
        descript= product.descript,
        price= product.price
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
     
    
    
##### Banner #####

#Crear registro
def new_register_banner(db:Session, data:BannerProductRequest):
    new_data = MBanner(title= data.title,
                       description= data.description)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return True

#Obtener datos de la base de datos 
def get_all_banners(db: Session, skip:int = 0, limit: int = 100):
    return db.query(MBanner).offset(skip).limit(limit=limit).all()

#Obtener dato de la base de datos por id 
def get_id_banner(db:Session, id:int):
    return  db.query(MBanner).filter(MBanner.id == id).first()

#Actualizar datos del banner
def update_banner(db:Session, id:int, data:BannerProductRequest):
    banner_db = db.query(MBanner).filter(MBanner.id == id).first()
    if not banner_db:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    banner_db.title = data.title
    banner_db.description = data.description
    db.commit()
    return banner_db

#Eliminar un registo del banner
def delete_banner(db:Session, id:int):
    banner_db = db.query(MBanner).filter(MBanner.id == id).first()
    if not banner_db:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    db.delete(banner_db)
    db.commit()
    
    
    
    