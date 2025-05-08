from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.config.db import SessionLocal
from app.pyd import Token, UserCreate, UserInDB
from app.services.auth_services import create_user, get_user_by_login
from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_user
)
from app.auth import get_db
from sqlalchemy.orm import Session
from app.config.config import settings


router = APIRouter(tags=['auth'])


@router.post("/token", response_model=Token)
async def login_for_access_token(
                    form_data: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate,
                    db: Session = Depends(get_db)):
    db_user = get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    return create_user(db=db, user=user)


@router.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user