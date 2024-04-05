from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from .oauth2 import authenticate_user, create_token
from .db import admin_user_db
from .schemes import Token


admin_router= APIRouter()

@admin_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user= authenticate_user(admin_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username o password incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires= timedelta(minutes=30)
    access_token_jwt=  create_token(data={"sub": user.username}, time_expire=access_token_expires)
    return Token(access_token=access_token_jwt, token_type="Bearer")