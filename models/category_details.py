from db import Base
from sqlalchemy import Column, String, Integer, and_, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from models.categories import Categories
from models.measures import Measures
from models.users import Users
from models.stages import Stages


class Category_details(Base):
    __tablename__ = 'category_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Numeric, nullable=False)
    measure_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    stage_id = Column(Integer)
    comment = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Category_details.user_id))
    measure = relationship('Measures', foreign_keys=[measure_id],
                           primaryjoin=lambda: and_(Measures.id == Category_details.measure_id))
    category = relationship('Categories', foreign_keys=[category_id],
                           primaryjoin=lambda: and_(Categories.id == Category_details.category_id))
    stage = relationship('Stages', foreign_keys=[stage_id],
                           primaryjoin=lambda: and_(Stages.id == Category_details.stage_id))
