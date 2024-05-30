from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])


# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserDisplay])
def read_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Read one user by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserDisplay)
def read_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(db, id)


# Update a new user
@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)


# Delete a new user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)
