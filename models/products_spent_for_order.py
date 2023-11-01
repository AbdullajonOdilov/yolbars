from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.category_details import Category_details
from models.currencies import Currencies
from models.orders import Orders
from models.stages import Stages
from models.users import Users


class Products_spent_for_order(Base):
    __tablename__ = 'products_spent_for_order'
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer)
    category_detail_id = Column(Integer)
    stage_id = Column(Integer)
    currency_id = Column(Integer)
    user_id = Column(Integer)
    quantity = Column(Numeric)
    price = Column(Numeric)
    datetime = Column(DateTime)

    order = relationship("Orders", foreign_keys=[order_id],
                          primaryjoin=lambda: and_(Orders.id == Products_spent_for_order.order_id))
    category_detail = relationship("Category_details", foreign_keys=[category_detail_id],
                                   primaryjoin=lambda: and_(Category_details == Products_spent_for_order.category_detail_id))
    stage = relationship("Stages", foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Products_spent_for_order.stage_id))
    currency = relationship("Currencies", foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Products_spent_for_order.currency_id))
    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Products_spent_for_order.user_id))
