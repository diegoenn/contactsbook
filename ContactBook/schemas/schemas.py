import datetime

from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    fullname: Optional[str]
    phone_number: Optional[int]
    email: Optional[str]
    direction: Optional[str]


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: Optional[int]
    owner_contact: Optional[int]
    date_created: Optional[datetime.datetime]

    class Config:
        orm_mode = True
