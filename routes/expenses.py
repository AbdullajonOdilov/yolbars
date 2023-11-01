import inspect
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from functions.expenses import one_expense, all_expenses, create_expense, update_expense
from routes.login import get_current_active_user
from schemes.expenses import CreateExpense, UpdateExpense
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses Endpoints"]
)


@expenses_router.get('/all')
def get_expenses(source: str = None, source_id: int = 0, id: int = 0, kassa_id: int = 0,
                 from_date: date = Query(None), to_date: date = Query(date.today()), page: int = 1,
                 limit: int = 25, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_expense(id, db)
    else:
        return all_expenses(source, source_id, kassa_id, from_date, to_date, page=page, limit=limit, db=db)


@expenses_router.post('/create')
def expense_create(form: CreateExpense,
                   db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_expense(form, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@expenses_router.put("/update")
def expense_update(form: UpdateExpense, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_expense(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


