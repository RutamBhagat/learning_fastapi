from typing import Optional
from fastapi import APIRouter, Depends, Request

from app.db.hash import Hash

router = APIRouter(
    prefix="/dependencies",
    tags=["dependencies"],
)


class Account:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = Hash.bcrypt(password)


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


@router.post("/user")
def create_user(
    name: str, email: str, password: str, account: Account = Depends(Account)
):
    # account - perform whatever operations you need to do with the account
    return {
        "name": account.name,
        "email": account.email,
        "password": account.password,
    }
