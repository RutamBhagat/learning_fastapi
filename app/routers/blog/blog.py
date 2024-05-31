from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas import BlogBase, BlogDisplay
from db import db_blog
from auth.oauth2 import oauth2_schema

router = APIRouter(prefix="/blog", tags=["blog"])


# Create a new blog
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BlogDisplay)
async def create_blog(request: BlogBase, db: Session = Depends(get_db)):
    print("request", request)
    return db_blog.create_blog(db, request)


# Get a blog by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogDisplay)
async def get_blog(
    id: int, token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    return db_blog.get_blog(db, id)


# Delete a blog by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: Session = Depends(get_db)):
    db_blog.delete_blog(db, id)
