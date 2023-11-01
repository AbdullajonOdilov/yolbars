from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *

from models.barcodes import Barcodes
from models.users import Users


class Broken_product_histories(Base):
    __tablename__ = 'broken_product_histories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    barcode_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    barcode = relationship("Barcodes", foreign_keys=[barcode_id],
                            primaryjoin=lambda: and_(Barcodes.id == Broken_product_histories.barcode_id))
    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Broken_product_histories.user_id))