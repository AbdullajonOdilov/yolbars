from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, and_

from models.categories import Categories
from models.measures import Measures
from models.users import Users


class Stages(Base):
    __tablename__ = 'stages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(565), nullable=False)
    number = Column(Integer, nullable=False, default=0)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    kpi = Column(Numeric, nullable=False)
    measure_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)

    measure = relationship("Measures", foreign_keys=[measure_id],
                           primaryjoin=lambda: and_(Measures.id == Stages.measure_id))
    category = relationship("Categories", foreign_keys=[category_id],
                           primaryjoin=lambda: and_(Categories.id == Stages.category_id))
    stage_user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Stages.user_id))
