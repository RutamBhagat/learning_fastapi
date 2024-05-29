from enum import Enum
from typing import Optional
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, Response

app = FastAPI()


class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "how-to"


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# @app.get("/blog/all")
# async def get_all_blogs():
#     return {"message": "All blogs in the database"}


# @app.get("/blog/all")
# async def get_all_blogs(limit: int = 10, published: bool = True):
#     return {"message": f"Blog with limit {limit} and published {published}"}


@app.get(
    "/blog/all",
    summary="Retrieve All Blogs",
    description="This API retrieves all blogs from the database",
    response_description="The list of all available blogs",
)
async def get_all_blogs(page: int = 1, page_size: Optional[int] = None):
    return {"message": f"Blog with page {page} and page_size {page_size}"}


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
async def get_blog(id: int, response: Response):
    if id > 10:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Blog not found!"}
    return {"message": f"Blog with id {id}"}


@app.get("/blog/{id}/comments/{comment_id}")
async def get_comment(
    id: int, comment_id: int, valid: bool = True, username: Optional[str] = None
):
    """Retrieve a comment with id from a blog with id"""
    return {
        "message": f"Comment with id {comment_id} from blog with id {id} is valid: {valid} and username: {username}"
    }


@app.get("/blog/type/{type}")
async def get_blog_by_type(type: BlogType):
    return {"message": f"Blog with type {type}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
