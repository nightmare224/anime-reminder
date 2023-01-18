from sqlalchemy import Column, String, ForeignKey
from lib.db.db_util import Base
from models.db.anime import Anime_DB

class User_DB(Base):
    __tablename__ = 'user_profile'
    __table_args__ = ()
    user_id = Column(
        String(length = 64),
        unique = True, primary_key = True, nullable = False
    )

class User_Anime_DB(Base):
    __tablename__ = 'user_anime'
    __table_args__ = ()
    user_id = Column(
        String(length = 64),
        ForeignKey("user_profile.user_id", ondelete="CASCADE"),
        primary_key = True, nullable = False
    )
    anime_id = Column(
        String(length = 64),
        ForeignKey("anime_profile.anime_id", ondelete="CASCADE"),
        primary_key = True, nullable = False
    )