from db import Base
from sqlalchemy import Column, Integer, Boolean, and_
from sqlalchemy.orm import relationship

from models.orders import Orders
from models.stages import Stages


class Barcodes(Base):
    __tablename__ = 'barcodes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer, nullable=False)
    stage_id = Column(Integer, nullable=False)
    broken = Column(Boolean, default=False)

    stage = relationship("Stages", foreign_keys=[stage_id],
                        primaryjoin=lambda: and_(Stages.id == Barcodes.stage_id))
    order = relationship("Orders", foreign_keys=[order_id],
                         primaryjoin=lambda: and_(Orders.id == Barcodes.order_id),lazy='joined')
