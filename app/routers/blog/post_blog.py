from typing import Dict, List, Optional
from fastapi import APIRouter, Path, Query, Body
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])


class ImageModel(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str = "YOUR TITLE"
    content: str = "YOUR CONTENT"
    number_of_comments: Optional[int] = 0
    is_published: Optional[bool] = False
    tags: List[str] = []
    metadata: Dict[str, str] = {"Authon": "Anon", "Date": "01-01-2000"}
    image: Optional[ImageModel] = None


@router.post("/new")
def create_blog(blog: BlogModel):
    return {
        "message": f"""Blog is created successfully 
        Title: {blog.title} 
        Content: {blog.content} 
        Published: {blog.is_published}
        List of Tags: {blog.tags}
        Metadata: {blog.metadata}
        Image: {blog.image}"""
    }


@router.post("/new/{id}")
def create_blog_with_id(blog: BlogModel, id: int, version: int = 1):
    return {
        "message": f"""Blog is created successfully with 
        ID {id} 
        Version: {version} 
        Title: {blog.title} 
        Content: {blog.content} 
        Published: {blog.is_published}"""
    }


@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_id: int = Path(
        gte=0,
        lte=10,
        # alias="commentID", if you want to use it here you would have to change it in the endpoints above to camelCase as well
        deprecated=True,
        description="Some description for comment_id",
    ),
    remarks: str = Body(..., min_length=10, max_length=50, regex="^[a-z\s]*$"),
    v: Optional[List[float]] = Query([1.1, 2.2, 3.3]),
):
    return {
        "message": f"""Comment is created successfully with 
        ID {comment_id} 
        Blog ID {id} 
        Title: {blog.title} 
        Content: {blog.content} 
        Published: {blog.is_published} 
        Remarks: {remarks} 
        Versions: {v}"""
    }
