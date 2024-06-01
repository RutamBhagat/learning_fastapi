from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.db.database import engine
from app.db import models
from app.middlewares import time_middleware
from app.router import blog_get, blog_post, user, article, product, file
from app.templates import templates
from app.auth import authentication
from app.exceptions import StoryException
from app.client import html


app = FastAPI()

# Create a database connection
models.Base.metadata.create_all(engine)

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
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(time_middleware)  # this needs to be different from the one above


# Mount the static files directory
app.mount("/app/files", StaticFiles(directory="app/files"), name="files")
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")


# Endpoints
# redirect from / to /docs using fastapi redirect
# @app.get("/")
# async def root():
#     return RedirectResponse(url="/docs")


@app.get("/")
async def get_html():
    return HTMLResponse(html)


clients = []


## This is causing a deployment problem with render but the code works locally
## Deploy failed for 4187595: handle websocket disconnection
## Timed out
## Port scan timeout reached, no open ports detected. Bind your service to at least one port. If you don't need to receive traffic on any port, create a background worker instead.
# @app.websocket("/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             for client in clients:
#                 await client.send_text(data)
#     except WebSocketDisconnect:
#         clients.remove(websocket)
#         if not websocket.client_state.DISCONNECTED:
#             await websocket.close()


# Exceptions
@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#   return PlainTextResponse(str(exc), status_code=400)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # start command for deployment on render
    # uvicorn app.main:app --host 0.0.0.0 --port 8000
