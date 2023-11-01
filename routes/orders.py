import inspect
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from functions.orders import one_order, all_orders, create_order, update_order, order_delete, confirm_order
from routes.login import get_current_active_user
from schemes.orders import CreateOrder, UpdateOrder
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders Endpoints"]
)


@orders_router.get('/all')
def get_orders(id: int = 0, search: str = None, client_id: int = 0, user_id: int = 0, category_id: int = 0,
               currency_id: int = 0,
               from_date: date = Query(None), to_date: date = Query(date.today()), page: int = 1,
               limit: int = 25, db: Session = Depends(database),
               current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order(id, db)
    else:
        return all_orders(search, user_id, client_id, category_id, currency_id,
                          from_date, to_date, page, limit, db)


@orders_router.post('/create')
def order_create(form: CreateOrder,
                 db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_order(form, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.put("/update")
def order_update(form: UpdateOrder, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_order(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.delete("/delete")
def delete_order(id: int = 0, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    order_delete(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")



@orders_router.post("/confirm")
def order_confirm(id: int, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    confirm_order(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")