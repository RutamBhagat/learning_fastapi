from fastapi import APIRouter, Depends, Request
from app.db.hash import Hash
from custom_log import log

router = APIRouter(
    prefix="/dependencies", tags=["dependencies"], dependencies=[Depends(log)]
)


class Account:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = Hash.bcrypt(password)


def multi_level_dependency_func(request: Request, seperator: str = "--"):
    headers = []
    for key, value in request.headers.items():
        headers.append(f"{key} {seperator} {value}")
    return headers


def convert_headers(
    request: Request,
    seperator: str = "--",
    multi_dependency=Depends(multi_level_dependency_func),
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
