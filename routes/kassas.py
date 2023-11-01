import datetime
import inspect
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from functions.kassa import one_kassa, all_kassas, create_kassa, update_kassa
from routes.login import get_current_active_user
from schemes.kassa import CreateKassa, UpdateKassa
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
kassa_router = APIRouter(
    prefix="/kassa",
    tags=["Kassas Endpoints"]
)


@kassa_router.get('/all', status_code=200)
def get_kassas(currency_id: int = 0, search: str = None, id: int = 0,  page: int = 1,
               limit: int = 25, db: Session = Depends(database),
               current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_kassa(id, db)
    else:
        return all_kassas(currency_id=currency_id, search=search,
                          page=page, limit=limit, db=db)


@kassa_router.post('/create')
def kassa_create(form: CreateKassa, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_kassa(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@kassa_router.put("/update")
def kassa_update(form: UpdateKassa, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_kassa(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


