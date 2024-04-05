from pydantic import BaseModel
from datetime import datetime

class Products(BaseModel):
    id: int
    name: str
    type_product: str
    descript: str
    price: int
    creation_time: datetime


    class Config:
            from_attributes = True