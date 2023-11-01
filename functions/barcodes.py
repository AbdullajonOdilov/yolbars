from fastapi import HTTPException
from sqlalchemy import func

from models.barcodes import Barcodes
from models.stages import Stages
from models.categories import Categories
from utils.db_operations import save_in_db

from sqlalchemy.orm import joinedload
from sqlalchemy import and_

from utils.pagination import pagination


def all_barcodes(search, order_id, page, limit, db):
    barcodes = db.query(Barcodes).options(joinedload(Barcodes.stage))

    if search:
        search_formatted = "%{}%".format(search)
        barcodes = barcodes.filter(Categories.name.like(search_formatted))
    if order_id:
        barcodes = barcodes.filter(Barcodes.order_id == order_id)
    barcodes = barcodes.order_by(Barcodes.id.asc())
    return pagination(barcodes, page, limit)


def interval_barcodes(from_id, to_id, db):
    barcodes_query = db.query(Barcodes).options(joinedload(Barcodes.stage))

    if from_id and to_id:
        barcodes_query = barcodes_query.filter(and_(Barcodes.id >= from_id, Barcodes.id <= to_id))
    barcodes_query = barcodes_query.order_by(Barcodes.id.desc())

    barcodes = barcodes_query.all()
    return {"data": barcodes, "count": len(barcodes)}


def barcodes_for_info(order_id, db):
    barcodes = db.query(Barcodes, func.coalesce(func.count(Barcodes.id), 0).label("total_quantity")).\
        options(joinedload(Barcodes.stage).subqueryload(Stages.measure)).filter(Barcodes.order_id == order_id).\
        group_by(Barcodes.stage_id).all()
    return barcodes


def one_barcode(ident, db):
    the_item = db.query(Barcodes).filter(Barcodes.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def add_barcodes(quantity, order, db):
    for i in range(int(quantity)):
        new_broken_db = Barcodes(
            order_id=order.id,
            stage_id=0,
            broken=False
        )
        save_in_db(db, new_broken_db)


def update_barcode_stage_id(barcode_id, stage_id, db):
    db.query(Barcodes).filter(Barcodes.id == barcode_id).update({
        Barcodes.stage_id: stage_id
    })
    db.commit()


def delete_barcodes(order_id, db):
    barcodes = db.query(Barcodes).filter(Barcodes.order_id == order_id).all()
    for barcode in barcodes:
        db.query(Barcodes).filter(Barcodes.id == barcode.id).delete()
        db.commit()
