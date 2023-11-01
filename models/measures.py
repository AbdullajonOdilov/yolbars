from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func


class Measures(Base):
    __tablename__ = 'measures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)

