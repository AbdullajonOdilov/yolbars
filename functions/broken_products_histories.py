from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload, subqueryload

from functions.products import create_product
from models.barcodes import Barcodes
from models.stages import Stages
from models.products import Products
from models.broken_products_histories import Broken_product_histories
from models.categories import Categories
from models.orders import Orders
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_broken_products_histories(order_id, page, limit, db):
    broken_products_histories = db.query(Broken_product_histories).join(Broken_product_histories.barcode).options(
        joinedload(Broken_product_histories.user),
        joinedload(Broken_product_histories.barcode).options(subqueryload(Barcodes.order), subqueryload(Barcodes.stage).subqueryload(Stages.measure)))

    if order_id:
        broken_products_histories = broken_products_histories.filter(
            Barcodes.order_id == order_id)
    broken_products_histories = broken_products_histories.order_by(Broken_product_histories.id.desc())
    return pagination(broken_products_histories, page, limit)


def one_broken_p_history(ident, db):
    the_item = db.query(Broken_product_histories).join(Broken_product_histories.barcode).options(
        joinedload(Broken_product_histories.barcode).options(subqueryload(Barcodes.order))).filter(Broken_product_histories.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_broken_product_history(barcode_id, thisuser, db):
    barcode = db.query(Barcodes).filter(Barcodes.id == barcode_id, Barcodes.broken == False).first()
    if barcode is None :
        raise HTTPException(status_code=404, detail="Ushbu qr code braklar ro'yhatida")
    order = the_one(db, Orders, barcode.order_id)
    category_id = order.category_id
    '''brak mahsulotlarni barcode id lari'''
    new_brak_barcode = Broken_product_histories(
        barcode_id=barcode_id,
        user_id=thisuser.id,
    )
    save_in_db(db, new_brak_barcode)
    '''products ga qo'shilib ketadi'''
    create_product(category_id, order.id, 1, 'brak', db)
    '''barcode dagi broken=True'''
    db.query(Barcodes).filter(Barcodes.id == barcode_id).update({
        Barcodes.broken: True,
    })
    db.commit()



