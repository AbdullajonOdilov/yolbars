from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, and_

from models.users import Users


class Currencies(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    money = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Currencies.user_id))


