#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
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
        """
        Save the user to the database
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        user.session_id = ""
        user.reset_token = ""
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **arb_args) -> User:
        """
        Returns the first row found in the users table as filtered by
        the method's input arguments
        """
        for arg in arb_args:
            if arg not in User.__dict__:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**arb_args).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **arb_args) -> None:
        """
        Locate the user and update its attributes as passed in the
        arguments
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in arb_args.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise(ValueError)
            self._session.commit()
            return None
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None
        finally:
            return None
