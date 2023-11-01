from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload, subqueryload

from functions.barcodes import add_barcodes, delete_barcodes
from functions.kassa import one_kassa_via_currency_id

from models.categories import Categories
from models.clients import Clients
from models.currencies import Currencies
from models.incomes import Incomes
from models.order_done_products import Order_done_products
from models.orders import Orders
from models.products import Products


from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_orders(search, user_id, client_id, category_id, currency_id, from_date, to_date, page, limit, db):
    orders = db.query(Orders).join(Orders.category).options(
        joinedload(Orders.client).options(subqueryload(Clients.client_phones)), joinedload(Orders.currency),
        joinedload(Orders.user),
        joinedload(Orders.category))
    orders_for_price = db.query(Orders, func.sum(Orders.price * Orders.quantity).label("total_price")).options \
        (joinedload(Orders.currency))

    if search:
        search_formatted = f"%{search}%"
        orders = orders.filter(Categories.name.like(search_formatted))
        orders_for_price = orders_for_price.filter(Categories.name.like(search_formatted))
    if client_id:
        orders = orders.filter(Orders.client_id == client_id)
        orders_for_price = orders_for_price.filter(Orders.client_id == client_id)
    if user_id:
        orders = orders.filter(Orders.user_id == user_id)
        orders_for_price = orders_for_price.filter(Orders.user_id == user_id)
    if from_date and to_date:
        orders = orders.filter(func.date(Orders.date).between(from_date, to_date))
        orders_for_price = orders_for_price.filter(func.date(Orders.date).between(from_date, to_date))
    if category_id:
        orders = orders.filter(Orders.category_id == category_id)
        orders_for_price = orders_for_price.filter(Orders.category_id == category_id)
    if currency_id:
        orders = orders.filter(Orders.currency_id == currency_id)
        orders_for_price = orders_for_price.filter(Orders.currency_id == currency_id)

    orders = orders.order_by(Orders.delivery_date.asc())
    price_data = []
    orders_for_price = orders_for_price.group_by(Orders.currency_id).all()
    for order in orders_for_price:
        price_data.append({"total_price": order.total_price, "currency": order.Orders.currency.name})
    return {"data": pagination(orders, page, limit), "price_data": price_data}


def one_order(ident, db):
    the_item = db.query(Orders).options(
        joinedload(Orders.currency), joinedload(Orders.category), joinedload(Orders.user),
        joinedload(Orders.client).options(subqueryload(Clients.client_phones))).filter(Orders.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order(form, db, thisuser):
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)
    new_order_db = Orders(
        client_id=form.client_id,
        date=datetime.now(),
        quantity=form.quantity,
        production_quantity=form.production_quantity,
        category_id=form.category_id,
        price=form.price,
        currency_id=form.currency_id,
        delivery_date=form.delivery_date,
        order_status=False,
        user_id=thisuser.id,
    )
    save_in_db(db, new_order_db)
    one_kassa_via_currency_id(currency_id=form.currency_id, db=db)
    add_barcodes(form.production_quantity, new_order_db, db)


def update_order(form, thisuser, db):
    order = the_one(db, Orders, form.id)
    if order.order_status == True:
        raise HTTPException(status_code=400, detail="Bu order allaqachon tugatilgan")
    the_one(db, Clients, form.client_id)
    the_one(db, Categories, form.category_id)
    the_one(db, Currencies, form.currency_id)

    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.client_id: form.client_id,
        Orders.quantity: form.quantity,
        Orders.production_quantity: form.production_quantity,
        Orders.price: form.price,
        Orders.date: datetime.now(),
        Orders.currency_id: form.currency_id,
        Orders.category_id: form.category_id,
        Orders.delivery_date: form.delivery_date,
        Orders.order_status: False,
        Orders.user_id: thisuser.id
    })
    db.commit()


def order_delete(id, db):
    the_one(db, Orders, id)
    order_done = db.query(Order_done_products).filter(Order_done_products.order_id == id).first()
    if order_done is None:
        db.query(Orders).filter(Orders.id == id).delete()
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Bu order jaroyonda, o'chirib bo'lmaydi")


def confirm_order(order_id, db):
    order = the_one(db=db, model=Orders,id=order_id)
    order_products = db.query(Products, func.sum(Products.quantity).label(
        "total_product")).filter(Products.order_id == order_id).all()
    order_products_summ = db.query(Incomes, func.sum(Incomes.money).label(
        "total_product_summ")).filter(Incomes.source_id == order_id).all()
    if order_products_summ[0][1] is None:
        raise HTTPException(status_code=400, detail=f"Bu buyurtma uchun hali to'lov qilinmagan")

    if order_products_summ[0][1] < order.price*order.quantity:
        raise HTTPException(status_code=400, detail=f"To'lov to'liq amalga oshirilmagan ")

    order = the_one(db, Orders, order_id)
    if order_products[0][1] is None:
        raise HTTPException(status_code=400, detail=f"Hech qanday maxsulot tayyor bo'lmagan")
    elif order_products[0][1] == order.production_quantity:
        db.query(Orders).filter(Orders.id == order_id).update({
            Orders.order_status: True
        })
        db.commit()
        delete_barcodes(order_id=order_id, db=db)

    elif order_products[0][1] < order.production_quantity:
        differ = order.production_quantity - order_products[0][1]
        raise HTTPException(status_code=400, detail=f"{differ}ta maxsulot hali tugatilmagan")
    else:
        differ = order_products[0][1] - order.production_quantity
        raise HTTPException(status_code=400, detail=f"{differ}ta maxsulot ortiqcha kiritilgan")
