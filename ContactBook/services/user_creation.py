import passlib.hash

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jwt import encode, decode

from ContactBook.models import models
from ContactBook.schemas import schemas
from ContactBook.config.config import settings
from ContactBook.services import utils


def get_user_by_email(
        email: str,
        db: Session
):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(
        user: schemas.UserCreate,
        db: Session
):
    user = models.User(
        email=user.email,
        hashed_password=passlib.hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(
        email: str,
        password: str,
        db: Session
):
    user = get_user_by_email(
        email=email,
        db=db
    )
    if not user:
        return False
    if not user.verify_password(password):
        return False

    return user


def create_token(
        user: models.User
):
    user = schemas.User.from_orm(user)

    token = encode(user.dict(), settings.JWT_SECRET)

    return dict(
        access_token=token,
        token_type="bearer"
    )


def get_current_user(
        db: Session = Depends(utils.get_db),
        token: str = Depends(settings.TOKEN_URL)
):
    try:
        payload = decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHMS]
        )
        user = db.query(models.User).get(payload['id'])
    except:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return schemas.User.from_orm(user)
