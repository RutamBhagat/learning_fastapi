from sqlalchemy.orm import Session
from db.hash import Hash
from db.models import DBUser
from schemas import UserBase
from fastapi import HTTPException, status

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User with given id not found"
)


def create_user(db: Session, request: UserBase):
    # Handle the case where the user already exists
    new_user = DBUser(
        username=request.username,
        email=request.email,
        hashed_password=Hash().hash_password(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DBUser).all()


def get_user_by_id(db: Session, id: int):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise user_not_found
    return user


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise user_not_found
    user.username = request.username
    user.email = request.email
    user.hashed_password = Hash().hash_password(request.password)
    db.commit()
    db.refresh(user)
    return "User updated"


def delete_user(db: Session, id: int):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise user_not_found
    db.delete(user)
    db.commit()
    return "User deleted"
