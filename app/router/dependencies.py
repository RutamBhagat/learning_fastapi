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


def convert_params(request: Request, seperator: str = "--"):
    query = []
    for key, value in request.headers.items():
        query.append(f"{key} {seperator} {value}")
    return query


def convert_headers(
    request: Request, seperator: str = "--", multi_dependency=Depends(convert_params)
):
    return multi_dependency


@router.get("/")
async def get_items(headers=Depends(convert_headers)):
    return {"items": ["headphones", "keyboard", "mouse"], "headers": headers}


@router.post("/new")
async def create_item(seperator: str = "-->", headers=Depends(convert_headers)):
    return {"result": "New item created", "headers": headers}


@router.post("/user")
def create_user(name: str, email: str, password: str, account: Account = Depends()):
    # Use the account dependency to perform you operations
    return {
        "name": account.name,
        "email": account.email,
        "password": account.password,
    }
