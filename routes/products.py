import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from functions.products import one_product, all_products
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
products = APIRouter(
    prefix="/products",
    tags=["Products Endpoints"]
)


@products.get('/all')
def get_broken_products(id: int = 0, search: str = None, type: str = None, category_id: int = 0,  page: int = 1,
                        limit: int = 25, db: Session = Depends(database),
                        current_user: UserCurrent = Depends(get_current_active_user)
                        ):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_product(id, db)
    else:
        return all_products(search, type, category_id, page, limit, db)
