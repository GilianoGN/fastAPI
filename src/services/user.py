from databases.interfaces import Record
from src.database import database
from fastapi import HTTPException, status
from src.models.user import users
from src.schemas.user import UserIn, UserUpdateIn


class UserService:
    async def read_all(self, limit: int,
                       skip: int = 0) -> list[Record]:
        query = users.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, user: UserIn) -> int:
        command = users.insert().values(
            name=user.name,
            password=user.password,
        )
        return await database.execute(command)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def update(self, id: int, user: UserUpdateIn) -> Record:
        total = await self.count(id)
        if not total:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        data = user.model_dump(exclude_unset=True)
        command = users.update().where(users.c.id == id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        command = users.delete().where(users.c.id == id)
        await database.execute(command)

    async def count(self, id: int) -> int:
        query = "select count(id) as total from users where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total

    async def __get_by_id(self, id) -> Record:
        query = users.select().where(users.c.id == id)
        user = await database.fetch_one(query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
