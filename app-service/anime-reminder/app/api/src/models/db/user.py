from sqlalchemy import Column, String, Integer, ForeignKey
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
    index = Column(
        Integer, primary_key=True, autoincrement=True,
        nullable = False
    )
    user_id = Column(
        String(length = 64),
        ForeignKey("user_profile.user_id", ondelete="CASCADE"),
        nullable = False
    )
    anime_id = Column(
        String(length = 64),
        ForeignKey("anime_profile.anime_id", ondelete="CASCADE"),
        nullable = False
    )

class User_Anime_Reminder_DB(Base):
    __tablename__ = 'user_anime_reminder'
    __table_args__ = ()
    index = Column(
        Integer,
        ForeignKey("user_anime.index", ondelete="CASCADE"),
        primary_key=True, nullable = False
    )
    season = Column(
        String(length = 16),
        primary_key=True, nullable = False
    )
    episode = Column(
        String(length = 16),
        nullable = False
    )