import inspect
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from functions.order_for_masters import create_order_for_master, all_order_for_masters, \
    one_order_for_master, confirm_order_for_master, delete_order_for_masters
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.order_for_masters import CreateOrder_for_masters,UpdateOrder_for_masters
from db import database

from schemes.users import UserCurrent
order_for_masters_router = APIRouter(
    prefix="/order_for_masters",
    tags=["Order for masters operation"]
)


@order_for_masters_router.post('/add', )
def order_for_masters(form: CreateOrder_for_masters, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_order_for_master(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@order_for_masters_router.get('/', status_code=200)
def get_order_for_masters(stage_id: int = 0, order_id: int = 0,  id: int = 0, page: int = 1,
                          from_date: date = Query(None), to_date: date = Query(date.today()), status: bool = None,
                          limit: int = 25, user_id: int = 0, connected_user_id: int = 0, db: Session = Depends(database),
                          current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order_for_master(id, db)
    else:
        return all_order_for_masters(stage_id=stage_id, order_id=order_id, page=page, limit=limit, db=db,from_date=from_date,to_date=to_date, status=status, user_id=user_id, connected_user_id=connected_user_id)


@order_for_masters_router.post("/confirm")
def masters_confirm(id: int = 0, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    confirm_order_for_master(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@order_for_masters_router.delete("/delete")
def delete_order_for_master(id: int = 0, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_order_for_masters(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


