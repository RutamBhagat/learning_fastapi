from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import DBBlog
from exceptions import StoryException
from schemas import BlogBase

blog_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Blog with given id not found"
)


def create_blog(db: Session, request: BlogBase):
    if request.content.startswith("#Lottery"):
        raise StoryException("Scam and Spam category, content is not allowed")
    new_blog = DBBlog(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.user_id,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_blog(db: Session, id: int):
    blog = db.query(DBBlog).filter(DBBlog.id == id).first()
    if not blog:
        raise blog_not_found
    return blog


def delete_blog(db: Session, id: int):
    blog = db.query(DBBlog).filter(DBBlog.id == id).first()
    if not blog:
        raise blog_not_found
    db.delete(blog)
    db.commit()
