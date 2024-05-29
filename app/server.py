from enum import Enum
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

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


@app.get("/blog/all")
async def get_all_blogs(limit: int = 10, published: bool = True):
    return {"message": f"Blog with limit {limit} and published {published}"}


@app.get("/blog/{id}")
async def get_blog(id: int):
    return {"message": f"Blog with id {id} "}


@app.get("/blog/type/{type}")
async def get_blog_by_type(type: BlogType):
    return {"message": f"Blog with type {type}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
