from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import *

from models.currencies import Currencies
from models.kassa import Kassas
from models.orders import Orders
from models.users import Users


class Incomes(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric,  nullable=False)
    currency_id = Column(Integer, nullable=False)
    date = Column(DateTime)
    user_id = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    kassa_id = Column(Integer, nullable=False)
    comment = Column(String(255))

    currency = relationship("Currencies", foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Incomes.currency_id))
    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Incomes.user_id))
    order_source = relationship("Orders", foreign_keys=[source_id],
                                primaryjoin=lambda: and_(Orders.id == Incomes.source_id, Incomes.source=='order'), backref=backref("income"))
    kassa = relationship("Kassas", foreign_keys=[kassa_id],
                         primaryjoin=lambda: and_(Kassas.id == Incomes.kassa_id))





