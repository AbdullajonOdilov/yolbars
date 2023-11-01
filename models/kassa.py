from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.currencies import Currencies
from models.users import Users


class Kassas(Base):
    __tablename__ = 'kassas'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255))
    user_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    balance = Column(Numeric)

    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Kassas.user_id))

    currency = relationship("Currencies", foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Kassas.currency_id))

