from fastapi import HTTPException

from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.measures import Measures


def all_measures(search, page, limit, db):
    measures_query = db.query(Measures)
    if search:
        search_formatted = f"%{search}%"
        measures_query = measures_query.filter(Measures.name.ilike(search_formatted))
    else:
        measures_query = measures_query.filter(Measures.id > 0)

    measures_query = measures_query.order_by(Measures.id.desc())
    return pagination(measures_query, page, limit)


def create_measure(form, db, thisuser):
    the_one_model_name(db, Measures, form.name)
    new_measure_db = Measures(
        name=form.name,
        user_id=thisuser.id, )
    save_in_db(db, new_measure_db)


def update_measure(form,  thisuser, db):
    measure = the_one(db, Measures, form.id)
    if db.query(Measures).filter(Measures.name == form.name).first() and measure.name != form.name:
        raise HTTPException(status_code=400, detail=f"Bazada bunday name({form.name}) mavjud!")
    db.query(Measures).filter(Measures.id == form.id).update({
        Measures.name: form.name,
        Measures.user_id: thisuser.id
    })
    db.commit()
