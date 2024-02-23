#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """database clss
    """

    def __init__(self) -> None:
        """Initialize clss
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates a new user and saves it in DB
        """
        try:
            n_user = User(email=email, hashed_password=hashed_password)
            self._session.add(n_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            n_user = None
        return n_user

    def find_user_by(self, **kwargs) -> User:
        """
        takes in arbitrary keyword arguments that serves to identify
        the user object(atributes)
        """
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
        f_user = self._session.query(User).filter_by(**kwargs).first()
        if f_user is None:
            raise NoResultFound
        return f_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the user object attributes,taking user id as
        an argument ,and the attributes to update
        """
        upd_user = self.find_user_by(id=user_id)
        if upd_user is None:
            return
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            setattr(upd_user, key, value)
        self._session.commit()
        return None
