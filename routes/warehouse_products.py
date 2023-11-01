import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.warehouse_products import one_warehouse_p, all_warehouse_products
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

warehouse_products_router = APIRouter(
    prefix="/warehouse_products",
    tags=["Warehouse products Endpoints"]
)


@warehouse_products_router.get('/all')
def get_warehouse_products(id: int = 0, search: str = None, currency_id: int = 0,
                           category_detail_id: int = 0, page: int = 1,
                           limit: int = 25, db: Session = Depends(database),
                           current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_warehouse_p(id, db)
    else:
        return all_warehouse_products(search, currency_id, category_detail_id, page=page, limit=limit, db=db)
