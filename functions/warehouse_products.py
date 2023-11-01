from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload, subqueryload

from models.category_details import Category_details
from models.currencies import Currencies
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_warehouse_products(search, currency_id, category_detail_id, page, limit, db):
    warehouse_products = db.query(Warehouse_products).join(Warehouse_products.category_detail).options(
        joinedload(Warehouse_products.category_detail).options(subqueryload(Category_details.measure)),
        joinedload(Warehouse_products.currency))
    products_for_price = db.query(Warehouse_products, func.sum(Warehouse_products.quantity * Warehouse_products.price).label("total_price")).options(
        joinedload(Warehouse_products.currency))
    if search:
        search_formatted = "%{}%".format(search)
        warehouse_products = warehouse_products.filter(Category_details.name.like(search_formatted))
        products_for_price = products_for_price.filter(
            (Warehouse_products.quantity.like(search_formatted)) |
            (Warehouse_products.price.like(search_formatted))
        )
    if category_detail_id:
        warehouse_products = warehouse_products.filter(Warehouse_products.id == category_detail_id)
        products_for_price = products_for_price.filter(Warehouse_products.id == category_detail_id)
    if currency_id:
        warehouse_products = warehouse_products.filter(Warehouse_products.id == currency_id)
        products_for_price = products_for_price.filter(Warehouse_products.id == currency_id)
    warehouse_products = warehouse_products.order_by(Warehouse_products.id.desc())

    price_data = []
    products_for_price = products_for_price.group_by(Warehouse_products.currency_id).all()
    for w_product in products_for_price:
        price_data.append({"total_price": w_product.total_price, "currency": w_product.Warehouse_products.currency.name})
    return {"data": pagination(warehouse_products, page, limit), "price_data": price_data}


def one_warehouse_p(ident, db):
    the_item = db.query(Warehouse_products).join(Warehouse_products.category_detail).options(
        joinedload(Warehouse_products.currency),
        joinedload(Warehouse_products.category_detail).options(subqueryload(Category_details.measure))
    ).filter(Warehouse_products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_warehouse_product(category_detail_id, quantity, price, currency_id, db, thisuser):
    the_one(db, Category_details, category_detail_id)
    the_one(db, Currencies, currency_id)
    check = get_warehouse_product_with_price(category_detail_id=category_detail_id, db=db, price=price)
    if check:
        warehouse_quantity = check.quantity+quantity
        db.query(Warehouse_products).filter(Warehouse_products.category_detail_id == category_detail_id).update({
            Warehouse_products.quantity: warehouse_quantity,
            Warehouse_products.user_id: thisuser.id
        })
        db.commit()
    else:
        new_w_p_db = Warehouse_products(
            category_detail_id=category_detail_id,
            quantity=quantity,
            price=price,
            currency_id=currency_id,
        )
        save_in_db(db, new_w_p_db)


def update_warehouse_product(form, db, thisuser):
    the_one(db, Warehouse_products, form.id)
    the_one(db, Category_details, form.category_detail_id)
    the_one(db, Currencies, form.currency_id)
    db.query(Warehouse_products).filter(Warehouse_products.id == form.id).update({
        Warehouse_products.category_detail_id: form.category_detail_id,
        Warehouse_products.quantity: form.quantity,
        Warehouse_products.price: form.price,
        Warehouse_products.currency_id: form.currency_id,
        Warehouse_products.user_id: thisuser.id
    })
    db.commit()


def get_warehouse_product(category_detail_id, db):
    return db.query(Warehouse_products).filter(Warehouse_products.category_detail_id == category_detail_id).all()


def get_warehouse_product_with_price(category_detail_id, price, db):
    return db.query(Warehouse_products).filter(Warehouse_products.category_detail_id == category_detail_id, Warehouse_products.price == price).first()
