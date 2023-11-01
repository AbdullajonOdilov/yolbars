from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func, and_
from sqlalchemy.orm import relationship

from models.users import Users


class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255))
    user_id = Column(Integer, nullable=False)

    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Clients.user_id))


