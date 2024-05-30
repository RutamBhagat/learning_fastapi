from typing import List, Optional
from fastapi import APIRouter, Header, status
from fastapi.responses import Response, HTMLResponse, PlainTextResponse


router = APIRouter(prefix="/product", tags=["product"])

products = ["watch", "camera", "phone"]


@router.get("/all")
def get_all_products():
    # return products
    data = " ".join(products)
    return Response(content=data, media_type="text/plain")


@router.get("/with-header")
def get_products_with_header(
    response: Response, custom_header: Optional[List[str]] = Header(None)
):
    response.headers["custom_response_header"] = ", ".join(custom_header)
    return {"products": products, "custom_header": custom_header}


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"exmple": "<div>Product</div>"}},
            "description": "Returns the HTML for the product",
        },
        404: {
            "content": {"text/plain": {"exmple": "Product not available"}},
            "description": "A clear text error message",
        },
    },
)
def get_product(id: int):
    if id not in range(len(products)):
        return PlainTextResponse(
            content="Product not available",
            media_type="text/plain",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    product = products[id]
    output = f"""
                <head>
                    <style>
                        .product {{
                        width: 500px;
                        height: 30;
                        border: 1px insert green;
                        background-color: lightblue;
                        text-align: center;
                        }}
                    </style>
                    <body>
                        <div class='product'>{product}</div>
                    </body>
                </head>
            """
    return HTMLResponse(content=output, media_type="text/html")
