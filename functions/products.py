from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.products import Products
from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_products(search, type, category_id, page, limit, db):
    products = db.query(Products).join(Products.category).options(joinedload(Products.category))
    if type:
        products = products.filter(Products.type == type)
    if search:
        search_formatted = "%{}%".format(search)
        products = products.filter(Categories.name.like(search_formatted))
    if category_id:
        products = products.filter(Products.category_id == category_id)
    products = products.order_by(Products.id.desc())
    return pagination(products, page, limit)


def one_product(ident, db):
    the_item = db.query(Products).options(
        joinedload(Products.category)).filter(Products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_product(category_id, order_id, quantity, type, db):
    the_one(db, Categories, category_id)
    broken_product = db.query(Products).filter(Products.category_id == category_id, Products.type==type).first()
    if broken_product:
        new_quantity = broken_product.quantity + quantity
        db.query(Products).filter(Products.category_id == category_id, Products.type==type).update({
            Products.quantity: new_quantity,
            Products.order_id: order_id,
            Products.type: type
        })
        db.commit()
    else:
        new_broken_db = Products(
            category_id=category_id,
            order_id=order_id,
            quantity=quantity,
            type=type
        )
        save_in_db(db, new_broken_db)
    #quantity should be substract from cetegory_detail

