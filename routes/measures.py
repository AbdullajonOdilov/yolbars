import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.measures import create_measure, update_measure, all_measures
from models.measures import Measures
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.measures import MeasureCreate,MeasureUpdate
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
measures_router = APIRouter(
    prefix="/measures",
    tags=["Measure operation"]
)


@measures_router.post('/add', )
def add_measure(form: MeasureCreate, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_measure(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@measures_router.get('/', status_code=200)
def get_measures(search: str = None,  id: int = 0,  page: int = 1,
                 limit: int = 25, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return the_one(db, Measures, id)
    else:
        return all_measures(search=search, page=page, limit=limit, db=db, )


@measures_router.put("/update")
def measure_update(form: MeasureUpdate, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_measure(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


