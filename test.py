from sqlalchemy import func
from sqlalchemy.orm import Session

from db import SessionLocal
from models.broken_products_histories import Broken_product_histories


def confirm_order(order_id,db):

    order_products = db.query(Broken_product_histories,func.sum(Broken_product_histories.done_product_quantity + Broken_product_histories.brak_product_quantity).label("total_product")).filter(Broken_product_histories.order_id==order_id).all()
    print(order_products[0][1])
db: Session = SessionLocal()
confirm_order(order_id=2,db=db)