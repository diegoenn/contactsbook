from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException

from ContactBook.schemas import schemas
from ContactBook.models import models


def create_contact(
        user: schemas.User,
        db: Session,
        contact: schemas.ContactCreate
):
    contact = models.Contact(**contact.dict(), owner_contact=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return schemas.Contact.from_orm(contact)


def get_contacts(
        user: schemas.User,
        db: Session
):
    contacts = db.query(models.Contact)\
        .filter(models.Contact.owner_contact.like(user.id))

    return list(map(schemas.Contact.from_orm, contacts))


def get_contacts_by_filters(
        user: schemas.User,
        contact: schemas.Contact,
        db: Session
):
    filters = [key for key, value in dict(contact).items() if value is not None]

    if not filters:
        contacts = db.query(models.Contact)\
            .filter(models.Contact.owner_contact.like(user.id))
    else:
        contacts = db.query(models.Contact)\
            .filter(models.Contact.owner_contact.like(user.id),
                    and_(or_(
                        models.Contact.fullname == contact.fullname,
                        models.Contact.phone_number == contact.phone_number,
                        models.Contact.email == contact.email,
                        models.Contact.direction == contact.direction,
                        models.Contact.id == contact.id,
                        models.Contact.date_created == contact.date_created
                    )))
    return list(map(schemas.Contact.from_orm, contacts))


def contact_selector(
        contact_id: int,
        user: schemas.User,
        db: Session
):
    contact = db.query(models.Contact)\
        .filter(models.Contact.owner_contact.like(user.id),
                and_(
                    models.Contact.id.like(contact_id)
                ))\
        .first()
    if contact is None:
        raise HTTPException(status_code=404, detail='Contact not found')
    return contact


def get_contact(
        contact_id: int,
        user: schemas.User,
        db: Session
):
    contact = contact_selector(
        contact_id=contact_id,
        user=user,
        db=db
    )

    return schemas.Contact.from_orm(contact)


def delete_contact(
        contact_id: int,
        user: schemas.User,
        db: Session
):
    contact = contact_selector(
        contact_id=contact_id,
        user=user,
        db=db
    )

    db.delete(contact)
    db.commit()

    return {'Contact successfully deleted'}


def update_contact(
        contact_id: int,
        contact: schemas.ContactCreate,
        user: schemas.User,
        db: Session
):
    contact_db = contact_selector(
        contact_id=contact_id,
        user=user,
        db=db
    )

    contact_db.fullname = contact.fullname
    contact_db.phone_number = contact.phone_number
    contact_db.email = contact.email
    contact_db.direction = contact.direction

    db.commit()
    db.refresh(contact_db)

    return schemas.Contact.from_orm(contact_db)
