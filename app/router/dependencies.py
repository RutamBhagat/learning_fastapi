from typing import Optional
from fastapi import APIRouter, Depends, Request

router = APIRouter(
    prefix="/dependencies",
    tags=["dependencies"],
)


def convert_headers(request: Request, seperator: str = "--"):
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} {seperator} {value}")
    return out_headers


@router.get("/")
async def get_items(headers=Depends(convert_headers)):
    return {"items": ["headphones", "keyboard", "mouse"], "headers": headers}


@router.post("/new")
async def create_item(seperator: str = "-->", headers=Depends(convert_headers)):
    # NOTE: The seperator is kind of flaky in swagger docs
    # default parameter values it shows "--" instead of "-->"
    # but when provided manually it works fine
    return {"result": "New item created", "headers": headers}
