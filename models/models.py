from sqlalchemy import Column, String, Integer

from .db import base

class MPorducts(base):
    __tablename__= "products"

    id= Column(Integer, primary_key=True)
    name= Column(String, nullable=True, unique=True)
    type_product= Column(String)
    descript= Column(String)
    price= Column(Integer)
    
    
    
    
# modelo para el banner en la base de datos 
class MBanner(base):
    __tablename__= "banner"
    
    id= Column(Integer, primary_key=True, nullable=True)
    title= Column(String)
    description= Column(String)