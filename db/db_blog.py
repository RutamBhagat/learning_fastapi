from sqlalchemy.orm import Session

from db.models import DBBlog
from schemas import BlogBase


def create_blog(db: Session, request: BlogBase):
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
    # Handle the case where the blog doesn't exist
    return blog


def delete_blog(db: Session, id: int):
    blog = db.query(DBBlog).filter(DBBlog.id == id).first()
    db.delete(blog)
    db.commit()
