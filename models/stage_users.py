from sqlalchemy.orm import relationship


from db import Base
from sqlalchemy import Column, Integer, and_

from models.stages import Stages
from models.users import Users


class Stage_users(Base):
    __tablename__ = 'stage_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    connected_user_id = Column(Integer, nullable=False)

    stage = relationship("Stages", foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Stage_users.stage_id))
    connected_user = relationship("Users", foreign_keys=[connected_user_id],
                         primaryjoin=lambda: and_(Users.id == Stage_users.connected_user_id))
    user = relationship("Users", foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Stage_users.user_id))



