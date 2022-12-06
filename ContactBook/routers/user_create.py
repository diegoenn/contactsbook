from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


from ContactBook.schemas import schemas
from ContactBook.services import utils, user_creation


router = APIRouter(
    prefix="/user_create",
    tags=["UserCreate"],
    responses={404: {"description": "Not found"}},
)


@router.post('/')
def create_user(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    new_user = user_creation.get_user_by_email(email=user.email, db=db)
    if new_user:
        raise HTTPException(status_code=400, detail='Email already in use')
    valid_email = utils.check_email(user.email)
    if not valid_email:
        raise HTTPException(status_code=400, detail='Not a valid email')

    user = user_creation.create_user(user=user, db=db)

    return user_creation.create_token(user)


@router.post('/token')
def generate_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(utils.get_db)
):
    user = user_creation.authenticate(
        email=form_data.username,
        password=form_data.password,
        db=db
    )
    if not user:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    return user_creation.create_token(user)


@router.get('/user/me', response_model=schemas.User)
def get_user(
        user: schemas.User = Depends(user_creation.get_current_user)
):
    return user
