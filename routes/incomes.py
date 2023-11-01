from datetime import date
import inspect


from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic.fields import Field
from sqlalchemy.orm import Session

from functions.incomes import one_income, all_incomes, add_income
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

incomes_router = APIRouter(
    prefix="/incomes",
    tags=["Incomes Endpoints"]
)


@incomes_router.get('/all')
def get_incomes(id: int = 0, kassa_id: int = 0, source: str = None, source_id: int = 0,
                from_date: date = Query(None), to_date: date = Query(date.today()),  page: int = 1,
                limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_income(id, db)
    else:
        return all_incomes(source, source_id, kassa_id, from_date, to_date, page=page, limit=limit, db=db)


@incomes_router.post('/create')
def create_income(money: float = 0.1, currency_id: int = 0,
                  source: str = None, source_id: int = 0, comment: str = None, kassa_id: int = 0,
                  db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)
                  ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    add_income(currency_id, money, source, source_id, kassa_id, comment, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli bajarildi")
