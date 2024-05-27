"""DB module
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar

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

    def add_user(self, email: str,
                 hashed_password: str) -> TypeVar("User"):
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

    def find_user_by(self, **arb_args):
        """
        Returns the first row found in the users table as filtered by
        the method's input arguments
        """
        user = self._session.query(User).filter_by(**arb_args).first()
        return user

    def update_user(self, user_id: int, **arb_args):
        """
        Locate the user and update its attributes as passed in the
        arguments
        """
        user = self.find_user_by(id=user_id)
        for key, value in arb_args.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise(ValueError)
        self._session.commit()
        return None
