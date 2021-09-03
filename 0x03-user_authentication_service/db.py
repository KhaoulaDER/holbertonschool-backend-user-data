#!/usr/bin/env python3
"""
DB model
0x08. User authentication service
holbertonschool-web_back_end
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """ DB class """

    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds user to db """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Description: Find a user by keyword argument
        Args:
            keyword argument([dict]): [user Input]
        Return:
            user instance if user exist or raise an Error
        """

        try:
            dec = list(kwargs.items())
            user = self._session.query(User).filter(
                getattr(User, dec[0][0]) == dec[0][1]).first()
        except InvalidRequestError:
            raise InvalidRequestError
        except AttributeError:
            raise NoResultFound
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Finds user record and updates attributes """
        user_record = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user_record, key):
                setattr(user_record, key, value)
            else:
                raise ValueError

        self._session.commit()
        return None
