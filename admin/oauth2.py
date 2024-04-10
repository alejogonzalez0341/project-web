from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Union

from datetime import datetime, timedelta
from jose import JWTError, jwt
from zoneinfo import ZoneInfo

from dotenv import dotenv_values

from passlib.hash import pbkdf2_sha256

from .schemes import PasswordUser, User, TokenData
from .db import admin_user_db

config_env= dotenv_values(".env")

SECRET_KEY = config_env["SECRET_KEY"]
ALGORITHM= config_env["ALGORITHM"]
TOKEN_SCONDS_EXP= config_env["TOKEN_SCONDS_EXP"]


oauth2_scheme= OAuth2PasswordBearer("/token")

def get_user(db, username: str):
    if username in db:
        user_list= db[username]
        return PasswordUser(**user_list)
    return []
    

def verify_password(plane_password, hash_password):
    return pbkdf2_sha256.verify(plane_password, hash_password)


def authenticate_user(db, username: str, password: str):
    user= get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No se pudieron validar las credenciales",
                            headers={"WWW-Authenticate": "Bearer"})
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No se pudieron validar las credenciales",
                            headers={"WWW-Authenticate": "Bearer"})
    
    return user



def create_token(data: dict, time_expire: Union[datetime, None]= None):
    data_copy= data.copy()
    if time_expire is None:
        expire= datetime.now(ZoneInfo("UTC")) + timedelta(minutes=15)
    else:
        expire= datetime.now(ZoneInfo("UTC")) + time_expire
    data_copy.update({"exp": expire})
    token_jwt= jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


async def get_user_current(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_decode= jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str= token_decode.get("sub")
        if username is None:
            raise credentials_exception
        token_data= TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user= get_user(admin_user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_user_disabled_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user
