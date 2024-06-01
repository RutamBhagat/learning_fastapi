import time
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db.database import engine
from app.db import models
from app.middlewares import time_middleware
from app.router import blog_get, blog_post, user, article, product, file
from app.templates import templates
from app.auth import authentication
from app.exceptions import StoryException


app = FastAPI()

# Routes
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(templates.router)

# Middlewares
app.middleware("http")(time_middleware)


# redirect from / to /docs using fastapi redirect
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#   return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/app/files", StaticFiles(directory="app/files"), name="files")
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# start command for deployment on render
# uvicorn app.main:app --host 0.0.0.0 --port 8000
