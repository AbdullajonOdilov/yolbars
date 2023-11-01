from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, DateTime, Numeric, Boolean, ForeignKey, and_

from models.category_details import Category_details
from models.currencies import Currencies
from models.suppliers import Suppliers
from models.users import Users


class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_detail_id = Column(Integer, nullable=False)
    quantity = Column(Numeric, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=True)
    status = Column(Boolean, nullable=True, default=False)
    received_user_id = Column(Integer, nullable=True)

    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.user_id))
    received_user = relationship("Users", foreign_keys=[received_user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.received_user_id))
    supplier = relationship("Suppliers", foreign_keys=[supplier_id],
                        primaryjoin=lambda: and_(Suppliers.id == Supplies.supplier_id))
    currency = relationship("Currencies", foreign_keys=[currency_id],
                        primaryjoin=lambda: and_(Currencies.id == Supplies.currency_id))

    category_detail = relationship('Category_details', foreign_keys=[category_detail_id],
                                   primaryjoin=lambda: and_(Category_details.id == Supplies.category_detail_id))