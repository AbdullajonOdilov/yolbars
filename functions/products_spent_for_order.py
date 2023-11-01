import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from models.category_details import Category_details
from models.currencies import Currencies
from models.orders import Orders
from models.products_spent_for_order import Products_spent_for_order
from models.stages import Stages
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


"Get all products spent for order"
def get_psfo(order_id, currency_id, stage_id, category_detail_id, page, limit, db):
    datas = db.query(Products_spent_for_order).options(joinedload(Products_spent_for_order.order),
                                                       joinedload(Products_spent_for_order.stage),
    # joinedload(Products_spent_for_order.category_detail),
                                                       joinedload(Products_spent_for_order.currency),
    joinedload(Products_spent_for_order.user))

    datas_stats = db.query(Products_spent_for_order,
                     func.sum(Products_spent_for_order.quantity * Products_spent_for_order.price
                              )).label("total_quantity").options(joinedload(Products_spent_for_order.order),
                                                                 joinedload(Products_spent_for_order.stage),
                                                                 joinedload(Products_spent_for_order.category_detail),
                                                                 joinedload(Products_spent_for_order.currency),
                                                                 joinedload(Products_spent_for_order.user))
    if order_id:
        datas = datas.filter(Products_spent_for_order.order_id == order_id)
        datas_stats = datas_stats.filter(Products_spent_for_order.order_id == order_id)
    if currency_id:
        datas = datas.filter(Products_spent_for_order.currency_id == currency_id)
        datas_stats = datas_stats.filter(Products_spent_for_order.currency_id == currency_id)
    if stage_id:
        datas = datas.filter(Products_spent_for_order.stage_id == stage_id)
        datas_stats = datas_stats.filter(Products_spent_for_order.stage_id == stage_id)
    if category_detail_id:
        datas = datas.filter(Products_spent_for_order.category_detail_id == category_detail_id)
        datas_stats = datas_stats.filter(Products_spent_for_order.category_detail_id == category_detail_id)

    datas = datas.order_by(Products_spent_for_order.id.desc())
    price_data = []
    datas_stats = datas_stats.\
        group_by(Products_spent_for_order.stage_id).group_by(Products_spent_for_order.order_id).\
        group_by(Products_spent_for_order.currency_id).group_by(Products_spent_for_order.category_detail_id).all()
    for stat in datas_stats:
        price_data.append({"total_quantity": stat.total_quantity, "stage": stat.Products_spent_for_order.stage.name,
                           "order": stat.Products_spent_for_order.order_id,
                           "category_detail_id":stat.Products_spent_for_order.category_detail.name,
                           "currency": stat.Products_spent_for_order.currency.name})
    return {"data": pagination(datas, page, limit), "price_data": price_data}


def create_psfo(order_id, category_detail_id, stage_id, currency_id, user_id, quantity, price, db):
    the_one(db, Orders, order_id)
    the_one(db, Category_details, category_detail_id)
    the_one(db, Stages, stage_id)
    the_one(db, Currencies, currency_id)
    check = db.query(Products_spent_for_order).filter(Products_spent_for_order.order_id == order_id,
        Products_spent_for_order.category_detail_id == category_detail_id, Products_spent_for_order.currency_id == currency_id,
        Products_spent_for_order.stage_id == stage_id, Products_spent_for_order.price == price, Products_spent_for_order.user_id == user_id).first()

    if check:
        psfo_quantity = Products_spent_for_order.quantity + quantity
        db.query(Products_spent_for_order).filter(Products_spent_for_order.order_id == order_id,
        Products_spent_for_order.category_detail_id == category_detail_id, Products_spent_for_order.currency_id == currency_id,
        Products_spent_for_order.stage_id == stage_id, Products_spent_for_order.price == price, Products_spent_for_order.user_id == user_id).update({
            Products_spent_for_order.quantity: psfo_quantity
        })
        db.commit()
    else:
        new_products_sfo = Products_spent_for_order(
            order_id = order_id,
            category_detail_id = category_detail_id,
            stage_id = stage_id,
            currency_id = currency_id,
            user_id = user_id,
            quantity = quantity,
            price = price,
            datetime = datetime.datetime.now()
        )
        save_in_db(db, new_products_sfo)

    raise HTTPException(status_code=200, detail="Amaliyot muvvaffaqiyatli bajarildi")


