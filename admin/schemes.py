from pydantic import BaseModel


class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class PasswordUser(User):
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None