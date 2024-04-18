from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from datetime import timedelta

from dotenv import dotenv_values

from .oauth2 import authenticate_user, create_token
from .db import admin_user_db
from .schemes import Token

config_env= dotenv_values(".env")

TOKEN_SCONDS_EXP= config_env["TOKEN_SCONDS_EXP"]

admin_router= APIRouter()

@admin_router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user= authenticate_user(admin_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username o password incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires= timedelta(seconds=10)
    access_token_jwt=  create_token(data={"sub": user.username}, time_expire=access_token_expires)
    return RedirectResponse("admin",
                            status_code=status.HTTP_302_FOUND,
                            headers={"set-cookie": f"access_token={access_token_jwt}; Max-Age={TOKEN_SCONDS_EXP}"}
                            )
    #return Token(access_token=access_token_jwt, token_type="Bearer")