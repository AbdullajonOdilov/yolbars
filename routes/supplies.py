import inspect
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session
from functions.supplies import create_supply, update_supply, all_supplies, delete_supply, one_supply, supply_confirm

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.supplies import SuppliesCreate, SuppliesUpdate, SuppliesConfirm
from db import database
from typing import List

from schemes.users import UserCurrent
supplies_router = APIRouter(
    prefix="/supplies",
    tags=["Supplies operation"]
)


@supplies_router.post('/add')
def add_supply(form: SuppliesCreate, db: Session = Depends(database),current_user:
               UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_supply(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.get('/', status_code=200)
def get_supplies(search: str = None,  id: int = 0,
                 category_detail_id: int = 0, supplier_id: int = 0,
                 from_date: date = Query(None),
                 to_date: date = Query(date.today()),
                 currency_id: int = 0, status: bool = None, page: int = 1,
                 limit: int = 25, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_supply(id, db)

    else:
        return all_supplies(search=search, from_date=from_date, to_date=to_date,
                            category_detail_id=category_detail_id,
                            supplier_id=supplier_id, currency_id=currency_id, status=status, page=page, limit=limit, db=db)


@supplies_router.put("/update")
def supply_update(form: SuppliesUpdate, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supply(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.post("/confirm")
def confirm_supply(ids: List[SuppliesConfirm], db: Session = Depends(database),
                   current_user:  UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    for id in ids:
        supply_confirm(id.id, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.delete("/delete")
def supply_delete(id: int, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_supply(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")