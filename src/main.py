from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import post, user, auth
from src.exceptions import NotFoundPostError, NotFoundUserError
from src.database import database
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "auth",
        "description": "Operações para autenticação.",
    },
    {
        "name": "posts",
        "description": "Operação para manutenção de posts.",
    },
    {
        "name": "users",
        "description": "Operação para manutenção de users.",
    },
]


servers = [
    {"url": "http://127.0.0.1:8000",
     "description": "Ambiente de desenvolvimento."},
    {"url": "https://fastapi-ez1r.onrender.com",
     "description": "Ambiente de produção."},
]


app = FastAPI(
    title="DIO Blog API",
    version="1.0.1",
    summary="API para blog pessoal",
    description="""
# 🚀 API para blog pessoal
API para criação de blog __pessoal__ com criação de usuarios,
totalmente _documentado_.
""",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    servers=servers,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router, tags=["posts"])
app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request,
                                           exc: NotFoundPostError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Post not found!"},
    )


@app.exception_handler(NotFoundUserError)
async def not_found_user_exception_handler(request: Request,
                                           exc: NotFoundUserError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found!"},
    )
