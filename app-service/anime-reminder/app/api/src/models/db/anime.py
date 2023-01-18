from sqlalchemy import Column, String
from lib.db.db_util import Base


class Anime_DB(Base):
    __tablename__ = 'anime_profile'
    __table_args__ = ()
    anime_id = Column(
        String(length = 64),
        unique = True, primary_key = True, nullable = False
    )
    anime_name = Column(
        String(length = 64), 
        nullable = False
    )