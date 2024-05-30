from sqlalchemy.orm import Session
from db.hash import Hash
from db.models import DBUser
from schemas import UserBase


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
    # Handle the case where the user doesn't exist
    return db.query(DBUser).filter(DBUser.id == id).first()


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    # Handle the case where the user doesn't exist
    if user:
        user.username = request.username
        user.email = request.email
        user.hashed_password = Hash().hash_password(request.password)
        db.commit()
        db.refresh(user)
        return "User updated"
    else:
        return None


def delete_user(db: Session, id: int):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    # Handle the case where the user doesn't exist
    if user:
        db.delete(user)
        db.commit()
        return "User deleted"
    else:
        return None
