import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from functions.clients import one_client, all_clients, create_client, update_client
from routes.login import get_current_active_user
from schemes.clients import CreateClient, UpdateClient
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent
client_router = APIRouter(
    prefix="/clients",
    tags=["Clients Endpoints"]
)


@client_router.get('/all_clients', status_code=200)
def get_clients(search: str = None, id: int = 0, page: int = 1,
                limit: int = 25, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_client(id, db)
    else:
        return all_clients(search, page, limit, db)


@client_router.post('/create')
def client_create(form: CreateClient, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_client(form=form, thisuser=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@client_router.put("/update")
def client_update(form: UpdateClient, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_client(form, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


