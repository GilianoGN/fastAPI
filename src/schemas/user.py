from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    password: str


class UserUpdateIn(BaseModel):
    name: str | None = None
    password: str | None = None
