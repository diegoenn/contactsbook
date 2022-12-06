from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from ContactBook.schemas import schemas
from ContactBook.services import user_creation, utils, contact_crud

router = APIRouter(
    prefix="/contacts",
    tags=["ManageContacts"],
    responses={404: {"description": "Not found"}},
)


@router.post('/', response_model=schemas.Contact)
def create_contact(
        contact: schemas.ContactCreate,
        user: schemas.User = Depends(user_creation.get_current_user),
        db: Session = Depends(utils.get_db)
):
    return contact_crud.create_contact(
        user=user,
        db=db,
        contact=contact
    )


@router.get('/', response_model=List[schemas.Contact])
def get_contacts(
        user: schemas.User = Depends(user_creation.get_current_user),
        db: Session = Depends(utils.get_db)
):
    return contact_crud.get_contacts(
        user=user,
        db=db
    )


@router.post('/filters')
def get_contact_by_filters(
        user: schemas.User = Depends(user_creation.get_current_user),
        contact: schemas.Contact = Depends(),
        db: Session = Depends(utils.get_db)
):
    return contact_crud.get_contacts_by_filters(
        user=user,
        contact=contact,
        db=db
    )


@router.get('/{contact_id}', status_code=200)
def get_contact(
        contact_id: int,
        user: schemas.User = Depends(user_creation.get_current_user),
        db: Session = Depends(utils.get_db)
):
    return contact_crud.get_contact(
        contact_id=contact_id,
        user=user,
        db=db
    )


@router.delete('/{contact_id}', status_code=200)
def delete_contact(
        contact_id: int,
        user: schemas.User = Depends(user_creation.get_current_user),
        db: Session = Depends(utils.get_db)
):
    return contact_crud.delete_contact(
        contact_id=contact_id,
        user=user,
        db=db
    )


@router.put('/{contact_id}', status_code=200)
def update_contact(
        contact_id: int,
        contact: schemas.ContactCreate,
        user: schemas.User = Depends(user_creation.get_current_user),
        db: Session = Depends(utils.get_db)
):
    contact_crud.update_contact(
        contact_id=contact_id,
        contact=contact,
        user=user,
        db=db
    )

    return {'message': 'Contact updated successfully'}
