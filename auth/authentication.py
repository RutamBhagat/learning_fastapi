from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.oauth2 import create_access_token
from db.database import get_db
from db.hash import Hash
from db.models import DBUser

router = APIRouter(tags=["authentication"])


@router.post("/token")
def get_token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    print("________________________AUTHENTICATION ENDPOINT HIT_____________________")
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = db.query(DBUser).filter(DBUser.username == request.username).first()
    if not user:
        raise unauthorized_exception
    is_password_matching = Hash().verify_password(
        request.password, user.hashed_password
    )
    if not is_password_matching:
        raise unauthorized_exception
    access_token = create_access_token(data={"sub": user.username})
    print(
        "TOKEN ENDPOINT: ",
        {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
        },
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }