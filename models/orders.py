from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.categories import Categories
from models.clients import Clients
from models.currencies import Currencies
from models.stages import Stages
from models.users import Users


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, autoincrement=True, primary_key=True)
    client_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    price = Column(Numeric)
    quantity = Column(Numeric)
    production_quantity = Column(Numeric)
    delivery_date = Column(Date, nullable=False)
    order_status = Column(Boolean, default=False)

    category = relationship("Categories", foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == Orders.category_id),lazy='joined')
    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Orders.user_id))
    client = relationship("Clients", foreign_keys=[client_id],
                          primaryjoin=lambda: and_(Clients.id == Orders.client_id))
    currency = relationship("Currencies", foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Orders.currency_id))

