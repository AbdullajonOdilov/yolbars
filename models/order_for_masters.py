from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, Float, DateTime, func, and_, Boolean

from models.orders import Orders
from models.stages import Stages
from models.users import Users


class Order_for_masters(Base):
    __tablename__ = 'order_for_masters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    user_id = Column(Integer,  nullable=False)
    connected_user_id = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    datetime = Column(DateTime, default=func.now(), nullable=False)
    confirm_date = Column(DateTime, nullable = True)
    status = Column(Boolean, default=False)

    stage = relationship("Stages", foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Order_for_masters.stage_id))
    order = relationship("Orders", foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Order_for_masters.order_id))
    user = relationship("Users", foreign_keys=[user_id],
                         primaryjoin=lambda: and_(Users.id == Order_for_masters.user_id))
    connected_user = relationship("Users", foreign_keys=[connected_user_id],
                         primaryjoin=lambda: and_(Users.id == Order_for_masters.connected_user_id))

