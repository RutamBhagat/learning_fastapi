from enum import Enum
from typing import Optional
from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter(prefix="/blog", tags=["blog"])


class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "how-to"


# @router.get("/all")
# async def get_all_blogs():
#     return {"message": "All blogs in the database"}


# @router.get("/all")
# async def get_all_blogs(limit: int = 10, published: bool = True):
#     return {"message": f"Blog with limit {limit} and published {published}"}


@router.get(
    "/all",
    summary="Retrieve All Blogs",
    description="This API retrieves all blogs from the database",
    response_description="The list of all available blogs",
)
async def get_all_blogs(page: int = 1, page_size: Optional[int] = None):
    return {"message": f"Blog with page {page} and page_size {page_size}"}


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_blog(id: int, response: Response):
    if id > 10:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Blog not found!"}
    return {"message": f"Blog with id {id}"}


@router.get("/{id}/comments/{comment_id}", tags=["comments"])
async def get_comment(
    id: int, comment_id: int, valid: bool = True, username: Optional[str] = None
):
    """Retrieve a comment with id from a blog with id"""
    return {
        "message": f"Comment with id {comment_id} from blog with id {id} is valid: {valid} and username: {username}"
    }


@router.get("/type/{type}")
async def get_blog_by_type(type: BlogType):
    return {"message": f"Blog with type {type}"}
