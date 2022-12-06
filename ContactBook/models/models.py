import datetime

import passlib.hash

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from ContactBook.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    contacts = relationship('Contact', back_populates='user_owner')

    def verify_password(self, password: str):
        return passlib.hash.bcrypt.verify(password, self.hashed_password)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    owner_contact = Column(Integer, ForeignKey('users.id'))
    fullname = Column(String, nullable=False)
    phone_number = Column(Integer, nullable=False)
    email = Column(String)
    direction = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    user_owner = relationship('User', back_populates='contacts')
