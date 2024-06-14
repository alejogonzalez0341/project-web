from pydantic import BaseModel
from datetime import datetime

class ProductsCreate(BaseModel):
    id:int
    name: str
    type_product: str
    descript: str
    price: int
    
    class Config:
            from_attributes = True

                    
class GetProduct(BaseModel):
    id: int
    type_product: str
    descript: str
    price: int
    
    
#schema para posductos del banner
class BannerProductRequest(BaseModel):
    title:str
    description:str
    
class ResponseBanner(BannerProductRequest):
    id:int