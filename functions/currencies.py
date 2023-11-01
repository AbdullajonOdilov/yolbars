from fastapi import HTTPException

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.currencies import Currencies


def all_currencies(search, page, limit, db):
    currencies_query = db.query(Currencies)

    if search:
        search_formatted = f"%{search}%"
        currencies_query = currencies_query.filter(Currencies.name.ilike(search_formatted))

    currencies_query = currencies_query.order_by(Currencies.id.desc())
    return pagination(currencies_query, page, limit)


def create_currency(form, db, thisuser):
    the_one_model_name(db, Currencies, form.name)
    new_currencie_db = Currencies(
        name=form.name,
        money=form.money,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)


def update_currency(form, db, thisuser):
    currency = the_one(db, Currencies, form.id)
    currency_ver = db.query(Currencies).filter(Currencies.name == form.name).first()
    if currency_ver and currency_ver.id != currency.id:
        raise HTTPException(status_code=400, detail="Bu currency name bazada mavjud")
    db.query(Currencies).filter(Currencies.id == form.id).update({
        Currencies.name: form.name,
        Currencies.money: form.money,
        Currencies.user_id: thisuser.id
    })
    db.commit()

