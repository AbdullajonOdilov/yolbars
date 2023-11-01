import inspect
from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from functions.order_done_products import create_order_done_product, all_order_done_products, one_order_done_product, \
    create_order_done_barcode
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.order_done_products import CreateOrder_done_products
from db import database


from schemes.users import UserCurrent
order_done_products_router = APIRouter(
    prefix="/order_done_products",
    tags=["Order done products operation"]
)


@order_done_products_router.post('/add', )
def add_done_products(form: CreateOrder_done_products, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return create_order_done_product(form=form, thisuser=current_user, db=db)


@order_done_products_router.get('/', status_code=200)
def get_order_done_products(stage_id: int = 0, order_id: int = 0, worker_id: int = 0,  id: int = 0, page: int = 1,
                    from_date: date = Query(None), to_date: date = Query(date.today()),
                    limit: int = 25, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order_done_product(id, db)
    else:
        return all_order_done_products(stage_id=stage_id, order_id=order_id,worker_id=worker_id, page=page, limit=limit, db=db,from_date=from_date,to_date=to_date)


@order_done_products_router.post('/create')
def create_barcode(barcode_id: int = Form(...), token: str = Form(...),  db: Session = Depends(database)):

    return create_order_done_barcode(barcode_id, token, db)
