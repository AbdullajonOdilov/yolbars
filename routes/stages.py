import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.stages import create_stage, update_stage, all_stages, one_stage
from models.stages import Stages
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.stages import CreateStage, UpdateStage
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
stages_router = APIRouter(
    prefix="/stages",
    tags=["Stage operation"]
)


@stages_router.post('/add', )
def add_stage(form: CreateStage, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@stages_router.get('/', status_code=200)
def get_stages(search: str = None, measure_id: int = 0, category_id: int = 0,
               id: int = 0, page: int = 1,
               limit: int = 25, db: Session = Depends(database),
               current_user: UserCurrent = Depends(get_current_active_user)
               ):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_stage(id, db)
    else:
        return all_stages(measure_id, category_id, search=search, page=page, limit=limit, db=db)


@stages_router.put("/update")
def stage_update(form: UpdateStage, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_stage(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


