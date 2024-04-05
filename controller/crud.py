from sqlalchemy.orm import Session

from models.models import MPorducts
from models.schemas import Products


def get_id(db:Session, id:int):
    db.query(MPorducts).filter(MPorducts.id == id).first()


def created_product(db: Session, products= Products):
    product= MPorducts(
        name= products.name,
        type_product= products.type_product,
        descript= products.descript,
        price= products.price,
        creation_time= products.creation_time
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



def get_all_products(db: Session, skip:int = 0, limit: int = 100):
    return db.query(MPorducts).offset(skip).limit(limit=limit).all()
