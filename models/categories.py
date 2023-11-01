from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, Integer, String, Boolean


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(999), nullable=False)
    status = Column(Boolean, nullable=False,default=True)
    user_id = Column(Integer, nullable=False)