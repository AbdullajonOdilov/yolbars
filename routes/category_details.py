import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.category_details import create_category_detail, update_category_detail, all_category_details, \
    one_category_detail
from models.category_details import Category_details
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.category_details import Category_detailsCreate,Category_detailsUpdate
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
category_details_router = APIRouter(
    prefix="/category_details",
    tags=["Category_details operation"]
)

@category_details_router.post('/add', )
def add_category_detail(form: Category_detailsCreate,
                        db: Session = Depends(database),
                        current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_category_detail(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@category_details_router.get('/', status_code=200)
def get_category_details(search: str = None,  id: int = 0, stage_id: int = 0, measure_id: int = 0,
                         category_id: int = 0, page: int = 1,
                         limit: int = 25, db: Session = Depends(database),
                         current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_category_detail(id, db)

    else:
        return all_category_details(search=search, stage_id=stage_id, measure_id=measure_id, category_id=category_id,
                                    page=page, limit=limit, db=db)


@category_details_router.put("/update")
def category_detail_update(form: Category_detailsUpdate, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_category_detail(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


