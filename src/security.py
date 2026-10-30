import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

SECRET = "my-secret"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


def sign_jwt(user_id: int) -> dict:
    now = time.time()
    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": str(user_id),
        "aud": "curso-fastapi",
        "exp": now + (60 * 30),  # 30 minutos
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


async def decode_jwt(token: str) -> dict | None:
    # try:
    decoded_token = jwt.decode(token, SECRET,
                               algorithms=[ALGORITHM],
                               options={"verify_aud": False})
    #                               audience="curso-fastapi",
    #    _token = JWTToken.model_validate({"access_token": decoded_token})
    #    return _token if _token.access_token.exp >= time.time() else None
    if decoded_token.get("exp", 0) < time.time():
        return None
    return decoded_token
    # except Exception:
    #     return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid authentication scheme.")

            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid or expired token.")
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid authentication code.")


async def get_current_user(
        token: Annotated[dict, Depends(JWTBearer())]
        ) -> dict[str, int]:
    return {"user_id": int(token.get("sub"))}


def login_required(current_user: Annotated[dict[str, int],
                                           Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access denied")
    return current_user
