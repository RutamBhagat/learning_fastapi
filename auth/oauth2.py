import os
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = "CBFsGJJTXXFKi729i7kNKtHoHHNfY4w6eKoUlbaWbHE="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
