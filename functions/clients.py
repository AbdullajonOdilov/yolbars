from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, delete_phone
from models.phones import Phones
from utils.db_operations import the_one
from utils.pagination import pagination
from models.clients import Clients


def all_clients(search, page, limit, db):
    clients = db.query(Clients).join(Clients.client_phones).options(joinedload(Clients.user),
                                                                    joinedload(Clients.client_phones))

    if search:
        search_formatted = f"%{search}%"
        clients = clients.filter(Clients.name.like(search_formatted) | Phones.number.like(search_formatted))

    clients = clients.order_by(Clients.id.desc())
    return pagination(clients, page, limit)


def one_client(ident, db):
    the_item = db.query(Clients).options(
        joinedload(Clients.user), joinedload(Clients.client_phones)).filter(Clients.id == ident).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail="Bu id dagi ma'lumot bazada mavjud emas")
    return the_item


def create_client(form, db, thisuser):
    new_client_db = Clients(
        name=form.name,
        comment=form.comment,
        user_id=thisuser.id,
    )
    db.add(new_client_db)
    db.flush()

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'client', new_client_db.id, comment, thisuser.id, db, commit=False)

    db.commit()

    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli bajarildi")


def update_client(form, db, thisuser):
    the_one(db, Clients, form.id)
    db.query(Clients).filter(Clients.id == form.id).update({
        Clients.name: form.name,
        Clients.comment: form.comment,
        Clients.user_id: thisuser.id
    })

    #source client ga teng bo'lgan nomerni yangilash
    client_phones = db.query(Phones).filter(Phones.source_id == form.id).all()
    for phone in client_phones:
        delete_phone(id=phone.id, db=db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number=number, source='client', source_id=form.id, comment=comment, user_id=thisuser.id,
                         db=db, commit=False)
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")

