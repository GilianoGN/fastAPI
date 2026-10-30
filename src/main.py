from fastapi import FastAPI
from src.controllers import auth
from contextlib import asynccontextmanager
from src.database import database, engine, metadata
from src.controllers import post, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.post import posts  # noqa
    from src.models.user import users  # noqa

    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
