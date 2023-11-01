from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.stages import Stages
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.stage_users import Stage_users


def all_stage_user(stage_id, connected_user_id, search, role, page, limit, thisuser, db):
    stage_users_query = db.query(Stage_users).join(Stage_users.connected_user).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user))

    if search:
        search_formatted = f"%{search}%"
        search_filter = Users.name.ilike(search_formatted)
        stage_users_query = stage_users_query.filter(search_filter)
    if connected_user_id:
        stage_users_query = stage_users_query.filter(Stage_users.connected_user_id == connected_user_id)

    if stage_id:
        stage_users_query = stage_users_query.filter(Stage_users.stage_id == stage_id)
    if role:
        stage_users_query = stage_users_query.filter(Users.role == "stage_admin")

    # admin = db.query(Stage_users).filter(Stage_users.connected_user_id == thisuser.id).first()
    # stage_users = stage_users_query.filter(Stage_users.stage_id == admin.stage_id).all()
    # stage_users_query = stage_users_query.filter(Stage_users.stage_id == admin.stage_id)

    stage_users_query = stage_users_query.order_by(Stage_users.id.desc())
    return pagination(stage_users_query, page, limit)


def all_stage_user_for_stage_admin(search, page, limit, thisuser, db):
    stage_admin_query = db.query(Stage_users).filter(Stage_users.connected_user_id == thisuser.id).all()
    stages = db.query(Stages).filter(Stages.id.in_([stage_admin.stage_id for stage_admin in stage_admin_query])).all()
    stage_users = db.query(Stage_users).join(Stage_users.connected_user).options(joinedload(Stage_users.connected_user)).filter(Stage_users.stage_id.in_([stage.id
                                                                    for stage in stages]), Users.role == "stage_user")

    if search:
        search_formatted = f"%{search}%"
        search_filter = Users.name.ilike(search_formatted)
        stage_users = stage_users.filter(search_filter)
    return pagination(stage_users, page, limit)


def one_stage_user(id, db):
    the_item = db.query(Stage_users).options(
        joinedload(Stage_users.stage), joinedload(Stage_users.connected_user)).filter(Stage_users.id == id).first()
    if the_item is None:
        raise HTTPException(status_code=400, detail="Bunday ma'lumot bazada mavjud emas")
    return the_item


def create_stage_user(stage_id, connected_user_id, thisuser, db):
    stage = the_one(db, Stages, stage_id)
    user = the_one(db, Users, connected_user_id)
    if user.role not in ['stage_user', 'stage_admin']:
        raise HTTPException(status_code=400, detail="Bu connected_user ni roli hodimga teng emas")
    stages = db.query(Stages).filter(Stages.category_id == stage.category_id).all()
    stage_user = db.query(Stage_users).filter(Stage_users.stage_id.in_([stage.id for stage in stages]),
                                              Stage_users.connected_user_id == user.id).first()
    if stage_user:
        raise HTTPException(status_code=400, detail="Bu connected_user_id bog'langan")
    else:
        new_stage_user_db = Stage_users(
            stage_id=stage_id,
            connected_user_id=connected_user_id,
            user_id=thisuser.id, )
        save_in_db(db, new_stage_user_db)


def update_stage_user(form, thisuser, db):
    stage_user = the_one(db, Stage_users, form.id)
    stage = db.query(Stages).filter(Stages.id == stage_user.stage_id).first()
    user = the_one(db, Users, form.connected_user_id)
    if user.role not in ['stage_user', 'stage_admin']:
        raise HTTPException(status_code=400, detail="Bu connected_user ni roli hodimga teng emas")

    stages = db.query(Stages).filter(Stages.category_id == stage.category_id).all()
    stage_user_ver = db.query(Stage_users).filter(Stage_users.stage_id.in_([stage1.id for stage1 in stages]),
                                              Stage_users.connected_user_id == user.id).first()
    if stage_user_ver and stage_user_ver.id != stage_user.id:
        raise HTTPException(status_code=400, detail="Bu connected_user_id bog'langan")

    db.query(Stage_users).filter(Stage_users.id == form.id).update({
        Stage_users.connected_user_id: form.connected_user_id,
        Stage_users.user_id: thisuser.id
    })
    db.commit()


def delete_stage_user(stage_id, connected_user_id, db):
    the_one(db, Stages, stage_id)
    the_one(db, Users, connected_user_id)
    db.query(Stage_users).filter(
        Stage_users.stage_id == stage_id,
        Stage_users.connected_user_id == connected_user_id
    ).delete()
    db.commit()