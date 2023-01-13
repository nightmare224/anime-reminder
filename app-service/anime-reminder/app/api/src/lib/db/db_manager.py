import threading
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError
from lib.db.db_util import get_db_sessionmaker, Base
# from api.lib.exceptions import OtherConflict


DEFAULT_SESSION_NAME = "default"
Base = Base

class DBManager():

    singleton = None
    mutex = threading.Lock()

    def __init__(self):
        if self.initialized: return
        self.__conf = {}
        self.__session_dict = {}
        self.initialized = True

    def __new__(cls, *args, **kwargs):
        if not cls.singleton:
            with cls.mutex:
                if not cls.singleton:
                    cls.singleton = super().__new__(cls)

        return cls.singleton

    @property
    def initialized(self):
        try:
            return self._initialized
        except AttributeError: 
            return False
    @initialized.setter
    def initialized(self, initialized):
        self._initialized = initialized


    def db_uri(self, name, db_uri, **kwargs):
        self.__conf[name] = db_uri
        self.__session_dict[name] = get_db_sessionmaker(db_uri, **kwargs)
        return self

    def __get_session_maker(self, name=None):
        if self.__session_dict == None or self.__conf == None:
            raise Exception("__session_dict is null,please add dburi to dbmanager")
        if name == None:
            name = list(self.__session_dict.keys())[0]
        return self.__session_dict[name]

    @contextmanager
    def session_ctx(self, name=None):
        DBSession = self.__get_session_maker(name)
        session = DBSession()
        try:
            yield session
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise Exception
            # raise OtherConflict(e.orig.pgerror)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()