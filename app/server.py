from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import models
from db.database import engine
from app.routers.blog import blog
from app.routers.blog import get_blog
from app.routers.blog import post_blog
from app.routers.user import user
from app.routers import product
from exceptions import StoryException


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(blog.router)
app.include_router(get_blog.router)
app.include_router(post_blog.router)
app.include_router(product.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT, content={"detail": exc.name}
    )


## NOTE: This will override every other HTTPExceptions like 100, 200, 300, 400, 500, etc.
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: HTTPException):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
