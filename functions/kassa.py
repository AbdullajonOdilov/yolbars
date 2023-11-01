from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.kassa import Kassas
from utils.db_operations import the_one, the_one_model_name, save_in_db
from utils.pagination import pagination


def all_kassas(currency_id, search,page, limit, db):
    kassas = db.query(Kassas).options(joinedload(Kassas.user), joinedload(Kassas.currency))

    if search:
        search_formatted = f"%{search}%"
        kassas = kassas.filter(
            (Kassas.name.like(search_formatted)) |
            (Kassas.comment.like(search_formatted)))
    if currency_id:
        kassas = kassas.filter(Kassas.currency_id == currency_id)

    kassas = kassas.order_by(Kassas.id.desc())
    return pagination(kassas, page, limit)


def one_kassa(ident, db):
    the_item = db.query(Kassas).options(
        joinedload(Kassas.user), joinedload(Kassas.currency),
        joinedload(Kassas.kassa_phones)
    ).filter(Kassas.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu id dagi ma'lumot bazada mavjud emas")
    return the_item


def create_kassa(form, db, thisuser):
    the_one(db, Currencies, form.currency_id)
    the_one_model_name(db, Kassas, form.name)
    new_kassa_db = Kassas(
        name=form.name,
        comment=form.comment,
        currency_id=form.currency_id,
        balance=0,
        user_id=thisuser.id,
    )
    save_in_db(db, new_kassa_db)


def update_kassa(form, thisuser,  db):
    kassa = the_one(db, Kassas, form.id)
    kassa_ver = db.query(Kassas).filter(Kassas.name == form.name).first()
    if kassa_ver and kassa_ver.id != kassa.id:
        raise HTTPException(status_code=400, detail="Bu kassa name bazada mavjud")
    db.query(Kassas).filter(Kassas.id == form.id).update({
        Kassas.name: form.name,
        Kassas.comment: form.comment,
        Kassas.user_id: thisuser.id,
    })
    db.commit()


def update_kassa_balance(money, kassa_id, db):
    db.query(Kassas).filter(Kassas.id == kassa_id).update({
        Kassas.balance: money
    })
    db.commit()


def one_kassa_via_currency_id(currency_id, db):
    the_item = db.query(Kassas).options(
        joinedload(Kassas.user), joinedload(Kassas.currency)
    ).filter(Kassas.currency_id == currency_id).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu currency dagi ma'lumot bazada mavjud emas")
    return the_item