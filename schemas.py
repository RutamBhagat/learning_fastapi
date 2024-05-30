from typing import List
from pydantic import BaseModel


# Blog inside UserDisplay
class Blog(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []

    class Config:
        from_attributes = True


# User inside BlogDisplay
class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class BlogBase(BaseModel):
    title: str
    content: str
    published: bool
    user_id: int


class BlogDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config:
        from_attributes = True
