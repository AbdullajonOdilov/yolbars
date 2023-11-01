from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, Float, DateTime, func, and_, Numeric

from models.orders import Orders
from models.stages import Stages
from models.users import Users


class Order_done_products(Base):
    __tablename__ = 'order_done_products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    worker_id = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    kpi_money = Column(Numeric)
    datetime = Column(DateTime, default=func.now(), nullable=False)

    stage = relationship("Stages", foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Order_done_products.stage_id))
    order = relationship("Orders", foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Order_done_products.order_id))
    user = relationship("Users", foreign_keys=[user_id],
                         primaryjoin=lambda: and_(Users.id == Order_done_products.user_id))
    worker = relationship("Users", foreign_keys=[worker_id],
                         primaryjoin=lambda: and_(Users.id == Order_done_products.worker_id))

