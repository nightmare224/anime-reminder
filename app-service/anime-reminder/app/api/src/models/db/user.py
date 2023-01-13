from sqlalchemy import Column, String
from lib.db.db_util import Base


class User_DB(Base):
    __tablename__ = 'user_profile'
    __table_args__ = ()
    user_id = Column(
        String(length = 64),
        unique = True, primary_key = True, nullable = False
    )