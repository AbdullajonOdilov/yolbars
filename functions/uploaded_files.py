import os
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from models.uploaded_files import Uploaded_files
from models.users import Users

from utils.db_operations import the_one


def one_file(ident, db):
    the_item = db.query(Uploaded_files).filter(Uploaded_files.id == ident).options(
        joinedload(Uploaded_files.user), joinedload(Uploaded_files.category).load_only(Categories.name)).first()
    if the_item is None:
        raise HTTPException(status_code=404, detail=f"Bazada bunday ma'lumot mavjud emas")
    return the_item


def create_file(new_files, source, source_id, comment, thisuser, db):
    if source not in ['category', "user"]:
        raise HTTPException(status_code=400, detail="Source error")

    if (source == "user" and the_one(db, Users, source_id)):
        uploaded_file_objects = []

        for new_file in new_files:
            file_location = f"Uploaded_files/{new_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(new_file.file.read())

            new_file_db = Uploaded_files(
                file=file_location,
                source=source,
                source_id=source_id,
                comment=comment,
                user_id=thisuser.id,
            )
            uploaded_file_objects.append(new_file_db)

        db.add_all(uploaded_file_objects)
        db.commit()
    elif (source == "category" and the_one(db, Categories, source_id)):
        uploaded_file_objects = []
        for new_file in new_files:
            file_location = f"Uploaded_files/{new_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(new_file.file.read())
            new_file_db = Uploaded_files(
                file=file_location,
                source=source,
                source_id=source_id,
                comment=comment,
                user_id=thisuser.id,
            )
            uploaded_file_objects.append(new_file_db)
        db.add_all(uploaded_file_objects)
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source va source_id bir biriga to'g'ri kelmadi")


def delete_file(id, db):
    file = the_one(db, Uploaded_files, id)
    db.query(Uploaded_files).filter(Uploaded_files.id == id).delete()
    os.unlink(file.file)
    db.commit()


def update_file(id, new_file, source, source_id, comment, thisuser, db):
    old_file = the_one(db, Uploaded_files, id)
    if source not in ['category', 'user']:
        raise HTTPException(status_code=400, detail="Source error")
    if (source == "category" and the_one(db, Categories, source_id)) \
            or source == "user" and (the_one(db, Users, source_id)):
        if new_file:
            file_location = f"Uploaded_files/{new_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(new_file.file.read())
            db.query(Uploaded_files).filter(Uploaded_files.id == id).update({
                Uploaded_files.file: file_location,
                Uploaded_files.source: source,
                Uploaded_files.source_id: source_id,
                Uploaded_files.comment: comment,
                Uploaded_files.user_id: thisuser.id
            })
            db.commit()
        if new_file is None:
            db.query(Uploaded_files).filter(Uploaded_files.id == id).update({
                Uploaded_files.file: old_file.file,
                Uploaded_files.source: source,
                Uploaded_files.source_id: source_id,
                Uploaded_files.comment: comment,
                Uploaded_files.user_id: thisuser.id
            })
            db.commit()

    else:
        raise HTTPException(status_code=400, detail="source va source_id bir biriga to'g'ri kelmadi")




