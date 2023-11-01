from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import Column, Integer, String, and_

from models.clients import Clients
from models.suppliers import Suppliers
from models.users import Users


class Phones(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(16), nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)

    #source id boglanish kerak bo'lganlar
    created_user = relationship('Users', foreign_keys=[user_id],
                                primaryjoin=lambda: and_(Users.id == Phones.user_id))

    this_user = relationship('Users', foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Users.id == Phones.source_id, Phones.source == "user"),
                             backref=backref("user_phones"))

    this_client = relationship('Clients', foreign_keys=[source_id],
                                primaryjoin=lambda: and_(Clients.id == Phones.source_id,
                                                          Phones.source == "client"), backref=backref("client_phones"))

    this_supplier = relationship('Suppliers', foreign_keys=[source_id],
                                 primaryjoin=lambda: and_(Suppliers.id == Phones.source_id,
                                                          Phones.source == "supplier"), backref=backref("supplier_phones"))


