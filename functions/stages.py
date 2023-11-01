from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.measures import Measures
from utils.db_operations import save_in_db, the_one, the_one_model_name
from utils.pagination import pagination
from models.stages import Stages


def all_stages(measure_id, category_id, search, page, limit, db):
    stages_query = db.query(Stages).options(joinedload(Stages.category),
                                            joinedload(Stages.measure),
                                            joinedload(Stages.stage_user))
    if measure_id:
        stages_query = stages_query.filter(Stages.measure_id == measure_id)
    if category_id:
        stages_query = stages_query.filter(Stages.category_id == category_id)

    if search:
        search_formatted = f"%{search}%"
        search_filter = Stages.name.ilike(search_formatted)
        stages_query = stages_query.filter(search_filter)

    stages_query = stages_query.order_by(Stages.number.asc())

    return pagination(stages_query, page, limit)


def one_stage(id, db):
    the_item = db.query(Stages).options(
        joinedload(Stages.category), joinedload(Stages.measure),
        joinedload(Stages.stage_user)).filter(Stages.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bazada bunday malumot mavjud emas")
    return the_item


def create_stage(form, thisuser, db):
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    existing_stage = db.query(Stages).filter(
        Stages.name == form.name,
        Stages.category_id == form.category_id
    ).first()

    if existing_stage:
        # Handle the validation error (e.g., raise an exception)
        raise HTTPException(status_code=400, detail="Bu kategoriyada bu nomdagi jarayon allaqachon mavjud.")
    existing_stage = db.query(Stages).filter(Stages.category_id == form.category_id).order_by(
            Stages.number.desc()).first()
    next_number = existing_stage.number + 1 if existing_stage else 1
    # Create a new stage instance
    new_stage_db = Stages(
        name=form.name,
        number=next_number,
        kpi=form.kpi,
        comment=form.comment,
        status=True,
        measure_id=form.measure_id,
        category_id=form.category_id,
        user_id=thisuser.id,
    )
    # Save the new stage to the database
    save_in_db(db, new_stage_db)


def update_stage(form, thisuser, db):
    stage = the_one(db, Stages, form.id)
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    stage_ver = db.query(Stages).filter(Stages.name == form.name).first()
    if stage_ver and stage_ver.id != stage.id:
        raise HTTPException(status_code=400, detail="Bu stage name bazada mavjud")
    existing_stage = db.query(Stages).filter(
        Stages.name == form.name,
        Stages.category_id == form.category_id
    ).first()

    check_number = db.query(Stages).filter(Stages.category_id == form.category_id,
                                            Stages.number == form.number).first()
    if check_number is None:
        raise HTTPException(status_code=400, detail="Numberni xato kiritingiz")

    if existing_stage and stage.name != form.name:
        # Handle the validation error (e.g., raise an exception)
        raise ValueError("Bu kategoriyada bu nomdagi jarayon allaqachon mavjud.")
    if check_number.number == form.number:
        db.query(Stages).filter(Stages.id == check_number.id).update({
            Stages.number: stage.number
        })
        db.query(Stages).filter(Stages.id == stage.id).update({
            Stages.number: form.number
        })
        db.commit()

    if existing_stage and stage.category_id != form.category_id:
        raise HTTPException(status_code=400, detail="Bir xil category_id uchun number bir xil bo'laolmaydi")

    db.query(Stages).filter(Stages.id == form.id).update({
        Stages.name: form.name,
        Stages.number: form.number,
        Stages.comment: form.comment,
        Stages.kpi: form.kpi,
        Stages.status: form.status,
        Stages.measure_id: form.measure_id,
        Stages.category_id: form.category_id,
        Stages.user_id: thisuser.id
    })
    db.commit()
