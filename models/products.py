from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.categories import Categories


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False, default=0)
    quantity = Column(Numeric, nullable=False)
    type = Column(String(20))


    category = relationship("Categories", foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == Products.category_id))

