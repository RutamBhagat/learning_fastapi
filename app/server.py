from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers.blog import get_blog
from app.routers.blog import post_blog


app = FastAPI()

app.include_router(get_blog.router)
app.include_router(post_blog.router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
