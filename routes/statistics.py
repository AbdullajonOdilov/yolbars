import datetime
import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from functions.products_spent_for_order import get_psfo
from functions.statistics import order_statistics, total_stats
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
from datetime import date
statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Statistics operation"]
)


@statistics_router.get('/', status_code=200)
def get_order_statistics(order_id: int = 0, from_time: date = None, to_time: date = datetime.date.today(),
                         db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return order_statistics(order_id, from_time, to_time, db)


@statistics_router.get('/stats', status_code=200)
def total_statics(db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return total_stats(db)


@statistics_router.get('/products_spent_for_order', status_code=200)
def products_spent_for_order(order_id: int = 0, currency_id: int = 0,
                             stage_id: int = 0, category_detail_id: int = 0,
                             page: int = 0, limit: int = 25,
                             db: Session = Depends(database),
                             current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_psfo(order_id, currency_id, stage_id, category_detail_id, page, limit, db)

