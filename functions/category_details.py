from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination

from models.categories import Categories
from models.measures import Measures
from models.stages import Stages
from models.category_details import Category_details


def all_category_details(search, stage_id, measure_id, category_id, page, limit, db):
    category_details = db.query(Category_details).options(
        joinedload(Category_details.category),
        joinedload(Category_details.measure), joinedload(Category_details.stage))

    if search:
        search_formatted = "%{}%".format(search)
        category_details = category_details.name.like(search_formatted)
    if measure_id:
        category_details = category_details.filter(Category_details.measure_id == measure_id)
    if stage_id:
        category_details = category_details.filter(Category_details.stage_id == stage_id)
    if category_id:
        category_details = category_details.filter(Category_details.category_id == category_id)

    category_details = category_details.order_by(Category_details.id.desc())
    return pagination(category_details, page, limit)


def one_category_detail(id, db):
    the_item = db.query(Category_details).options(
        joinedload(Category_details.category),
        joinedload(Category_details.measure), joinedload(Category_details.stage)).filter(Categories.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bu malumot bazada mavjud")
    return the_item


def create_category_detail(form, db, thisuser):
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)
    stage = the_one(db, Stages, form.stage_id)
    if form.category_id != stage.category_id:
        raise HTTPException(status_code=400, detail="Bu jaroyon uchun bu kategoriya bog'lanmagan")

    # Check if a record with the same name and category_id already exists
    existing_record = db.query(Category_details).filter(
        Category_details.name == form.name,
        Category_details.category_id == form.category_id,
        Category_details.stage_id == form.stage_id
    ).first()

    if existing_record:
        # Handle the validation error (e.g., raise an exception)
        raise HTTPException(status_code=400, detail="Bu kategoriyada bu nomdagi detal allaqachon mavjud.")

    new_currencie_db = Category_details(
        name=form.name,
        quantity=form.quantity,
        measure_id=form.measure_id,
        category_id=form.category_id,
        stage_id=form.stage_id,
        comment=form.comment,
        user_id=thisuser.id, )
    save_in_db(db, new_currencie_db)


def update_category_detail(form,  thisuser, db):
    category_detail = the_one(db, Category_details, form.id)
    the_one(db=db, model=Measures, id=form.measure_id)
    the_one(db=db, model=Categories, id=form.category_id)

    stage = the_one(db, Stages, form.stage_id)
    if form.category_id != stage.category_id:
        raise HTTPException(status_code=400, detail="Bu jaroyon uchun bu kategoriya bog'lanmagan")

    # Check if a record with the same name and category_id already exists
    existing_record = db.query(Category_details).filter(
        Category_details.name == form.name,
        Category_details.category_id == form.category_id
    ).first()

    if existing_record and category_detail.name != form.name:
        # Handle the validation error (e.g., raise an exception)
        raise ValueError("Bu kategoriyada bu nomdagi detal allaqachon mavjud.")
    db.query(Category_details).filter(Category_details.id == form.id).update({
        Category_details.name: form.name,
        Category_details.quantity: form.quantity,
        Category_details.measure_id: form.measure_id,
        Category_details.category_id: form.category_id,
        Category_details.stage_id: form.stage_id,
        Category_details.comment: form.comment,
        Category_details.user_id: thisuser.id
    })
    db.commit()


def one_category_detail_via_category(category_id, db):
    the_item = db.query(Category_details).filter(Category_details.category_id == category_id).all()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bu malumot bazada mavjud")
    return the_item