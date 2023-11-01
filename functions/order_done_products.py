import datetime

from fastapi import HTTPException
from sqlalchemy import func
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from functions.barcodes import update_barcode_stage_id
from functions.products import create_product
from functions.products_spent_for_order import create_psfo
from functions.users import add_user_balance
from models.barcodes import Barcodes
from models.categories import Categories
from models.category_details import Category_details
from models.order_done_products import Order_done_products
from models.orders import Orders
from models.warehouse_products import Warehouse_products
from models.stage_users import Stage_users
from models.stages import Stages
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_order_done_products(order_id, stage_id, worker_id, from_date, to_date, page, limit, db):
    order_done_products = db.query(Order_done_products).options(
        joinedload(Order_done_products.order), joinedload(Order_done_products.stage).subqueryload(Stages.measure),
        joinedload(Order_done_products.user), joinedload(Order_done_products.worker))
    order_done_product_stats = db.query(Order_done_products, func.sum(Order_done_products.quantity).label(
        "total_quantity")).options(joinedload(Order_done_products.stage), joinedload(Order_done_products.order))

    if order_id:
        order_done_products = order_done_products.filter(Order_done_products.order_id == order_id)
        order_done_product_stats = order_done_product_stats.filter(Order_done_products.order_id == order_id)
    if worker_id:
        order_done_products = order_done_products.filter(Order_done_products.worker_id == worker_id)
        order_done_product_stats = order_done_product_stats.filter(Order_done_products.worker_id == worker_id)
    if stage_id:
        order_done_products = order_done_products.filter(Order_done_products.stage_id == stage_id)
        order_done_product_stats = order_done_product_stats.filter(Order_done_products.stage_id == stage_id)
    if from_date and to_date:
        order_done_products = order_done_products.filter(
            func.date(Order_done_products.datetime).between(from_date, to_date))
        order_done_product_stats = order_done_product_stats.filter(func.date(Order_done_products.datetime).
                                                                   between(from_date, to_date))

    order_done_products = order_done_products.order_by(Order_done_products.id.desc())
    price_data = []
    order_done_product_stats = order_done_product_stats.\
        group_by(Order_done_products.stage_id).group_by(Order_done_products.order_id).all()
    for stat in order_done_product_stats:
        price_data.append({"total_quantity": stat.total_quantity, "stage": stat.Order_done_products.stage.name,
                           "order": stat.Order_done_products.order_id})
    return {"data": pagination(order_done_products, page, limit), "price_data": price_data}


def one_order_done_product(ident, db):
    the_item = db.query(Order_done_products).options(
        joinedload(Order_done_products.order), joinedload(Order_done_products.stage),
        joinedload(Order_done_products.user)).filter(Order_done_products.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_order_done_product(form, thisuser, db):
    user = the_one(db, Users, form.worker_id)
    barcode = the_one(db, Barcodes, form.barcode_id)
    if barcode.broken == True:
        raise HTTPException(status_code=400, detail='bu barcode brak mahsulotga tegishli')

    barcode_order = db.query(Orders).filter(Orders.id == barcode.order_id).first()
    category_stages = db.query(Stages).filter(Stages.category_id == barcode_order.category_id).order_by(Stages.number.asc()).first()

    stage = db.query(Stages).filter(Stages.id == category_stages.id).first()

    '''agar omborda shu kategory detailda yetarlicha bo'lsa amaliyot bajariladi, aks holda bajarilmaydi'''
    category_details = db.query(Category_details).filter(Category_details.stage_id == stage.id).all()
    for category_detail in category_details :
        warehouse_category_detail = db.query(Warehouse_products, func.sum(Warehouse_products.quantity).label("sum_quantity")).filter(Warehouse_products.category_detail_id
                                                                        == category_detail.id)
        if warehouse_category_detail.first().sum_quantity >= category_detail.quantity:
            category_detail_quantity = category_detail.quantity
            for item in warehouse_category_detail.group_by(Warehouse_products.id).all():

                """Adding datas to new database for Spent_products_for_order"""

                if item.Warehouse_products.quantity >= category_detail_quantity and category_detail_quantity > 0 :
                    db.query(Warehouse_products).filter(Warehouse_products.id == item.Warehouse_products.id).update({
                        Warehouse_products.quantity: Warehouse_products.quantity - category_detail_quantity
                    })
                    db.commit()
                    category_detail_quantity = 0
                elif item.Warehouse_products.quantity < category_detail_quantity and category_detail_quantity > 0 :
                    category_detail_quantity = category_detail_quantity - item.Warehouse_products.quantity
                    db.query(Warehouse_products).filter(
                        Warehouse_products.id == item.Warehouse_products.id).update({
                        Warehouse_products.quantity: 0
                    })
                    db.commit()
                """creating Spent_products_for_order"""
                # create_psfo(barcode.order_id, category_detail.id, barcode.stage_id, barcode_order.currency_id,
                #             thisuser.id, category_detail_quantity, barcode_order.price, db)
        else:
            raise HTTPException(status_code=400, detail="Omborda bu stage uchun yetarlicha detal mavjud emas")

    category = the_one(db, Categories, stage.category_id)
    stage_user = db.query(Stage_users).filter(Stage_users.connected_user_id == user.id).first()
    if barcode.stage_id == 0:
        stage_next = stage
    else :
        stage_b = db.query(Stages).filter(Stages.id == barcode.stage_id).first()
        stage_next = db.query(Stages).filter(Stages.category_id == category.id, Stages.number > stage_b.number).order_by(Stages.number.asc()).first()
    stage_last = db.query(Stages).filter(Stages.category_id == category.id).order_by(Stages.number.desc()).first()
    if stage_next is None or stage_user is None:
        raise HTTPException(status_code=400, detail="Bundan keyin jarayon mavjud emas")
    if stage_next.id != stage_user.stage_id:
        raise HTTPException(status_code=400, detail="Siz bu jarayonga biriktirilmagansiz")
    barcode = db.query(Barcodes).filter(Barcodes.id == form.barcode_id).first()
    if barcode.stage_id == stage_user.stage_id:

        raise HTTPException(status_code=400, detail="Bu bosqich bajarilgan")
    else:
        update_barcode_stage_id(barcode_id=barcode.id, stage_id=stage_user.stage_id, db=db)

    if stage_last.id == stage_user.stage_id:
        create_product(category.id, barcode.order_id, 1, "done", db)

    done_product = db.query(Order_done_products).filter(Order_done_products.order_id == barcode.order_id,
                                                        Order_done_products.stage_id == stage_user.stage_id,
                                                        Order_done_products.datetime == datetime.datetime.now().
                                                        date(), ).first()

    if not done_product:
        new_order_h_db = Order_done_products(
            order_id=barcode.order_id,
            datetime=datetime.datetime.now().date(),
            stage_id=stage_user.stage_id,
            worker_id=form.worker_id,
            quantity=1,
            kpi_money=stage.kpi,
            user_id=thisuser.id,
        )
        save_in_db(db, new_order_h_db)
    else:
        quantity = done_product.quantity + 1
        db.query(Order_done_products).filter(Order_done_products.order_id == barcode.order_id,
                                             Order_done_products.stage_id == stage_user.stage_id,
                                             Order_done_products.datetime == datetime.datetime.now().date(), ).update({
            Order_done_products.datetime: datetime.datetime.now().date(),
            Order_done_products.quantity: quantity,

        })
        db.commit()

    money = stage.kpi
    add_user_balance(user_id=form.worker_id, money=money, db=db)
    """worker   shu order bo'yicha nechta qilgani chiqishi kerak"""
    worker_quantity = db.query(Order_done_products, func.sum(Order_done_products.quantity)). \
        filter(Order_done_products.order_id == barcode.order_id, Order_done_products.worker_id == form.worker_id).all()
    return worker_quantity[0][1]


def create_order_done_barcode(barcode_id, token, db):
    user = db.query(Users).filter(Users.token == token).first()
    barcode = the_one(db, Barcodes, barcode_id)
    class form:
        barcode_id: int = barcode.id
        worker_id: int = user.id
        quantity: int = 1
    return create_order_done_product(form = form, thisuser = user, db = db)