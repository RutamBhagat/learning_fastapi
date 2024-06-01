import time
from typing import Optional, List
from fastapi import APIRouter, BackgroundTasks, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from custom_log import log

router = APIRouter(prefix="/product", tags=["product"])

products = ["watch", "camera", "phone"]


async def time_consuming_functionality(message: str, delay: int = 1):
    time.sleep(delay)
    print(f"{message} that took {delay} seconds")
    return "ok"


@router.post("/new")
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get("/all")
async def get_all_products(bt: BackgroundTasks):
    # await time_consuming_functionality()
    bt.add_task(
        time_consuming_functionality, message="Time consuming function called", delay=10
    )
    log(tag="MyAPI", message="Call to get all products")
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


@router.get("/withheader")
def get_products(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
):
    if custom_header:
        response.headers["custom_response_header"] = " and ".join(custom_header)
    return {"data": products, "custom_header": custom_header, "my_cookie": test_cookie}


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"example": "<div>Product</div>"}},
            "description": "Returns the HTML for an object",
        },
        404: {
            "content": {"text/plain": {"example": "Product not available"}},
            "description": "A cleartext error message",
        },
    },
)
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(status_code=404, content=out, media_type="text/plain")
    else:
        product = products[id]
        out = f"""
    <head>
      <style>
      .product {{
        width: 500px;
        height: 30px;
        border: 2px inset green;
        background-color: lightblue;
        text-align: center;
      }}
      </style>
    </head>
    <div class="product">{product}</div>
    """
        return HTMLResponse(content=out, media_type="text/html")
