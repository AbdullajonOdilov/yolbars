from db import Base
from sqlalchemy import Column, Integer, Numeric, and_,Boolean
from sqlalchemy.orm import relationship
from models.category_details import Category_details
from models.currencies import Currencies


class Warehouse_products(Base):
    __tablename__ = 'warehouse_products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_detail_id = Column(Integer, nullable=False)
    quantity = Column(Numeric)
    price = Column(Numeric)
    currency_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=True)

    category_detail = relationship('Category_details', foreign_keys=[category_detail_id],
                                   primaryjoin=lambda: and_(Category_details.id == Warehouse_products.category_detail_id))
    currency = relationship("Currencies", foreign_keys=[currency_id],
                            primaryjoin=lambda: and_(Currencies.id == Warehouse_products.currency_id))
