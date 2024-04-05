from sqlalchemy import Column, String, Integer, DateTime

from .db import base

class MPorducts(base):
    __tablename__= "products"

    id= Column(Integer, primary_key=True)
    name= Column(String)
    type_product= Column(String)
    descript= Column(String)
    price= Column(Integer)
    creation_time= Column(DateTime)