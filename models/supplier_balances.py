from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import Column, Integer, and_, Numeric

from models.currencies import Currencies
from models.suppliers import Suppliers


class Supplier_balance(Base):
    __tablename__ = 'supplier_balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Numeric, nullable=False)
    currencies_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)

    currency = relationship("Currencies", foreign_keys=[currencies_id],
                        primaryjoin=lambda: and_(Currencies.id == Supplier_balance.currencies_id))
    balances = relationship("Suppliers", foreign_keys=[supplier_id],
                            primaryjoin=lambda: and_(Suppliers.id == Supplier_balance.supplier_id),
                            backref=backref("supplier_balances"))

