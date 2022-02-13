from typing import Iterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entities.Item import Item
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from app.models.requests.ItemRequest import AddItemRequest, UpdateItemRequest


class ItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> Iterator[Item]:
        query = await self.session.execute(select(Item).order_by(Item.id))
        return query.scalars().all()

    async def get(self, id: int) -> Item:
        query = await self.session.execute(select(Item).where(Item.id == id))
        result = query.one_or_none()

        if not result:
            raise ItemNotFoundError(id)

        return result

    async def add(self, request: AddItemRequest) -> Item:
        entity = Item(id=request.id, name=request.name, description=request.description)

        try:
            self.session.add(entity)
            await self.session.flush()
        except IntegrityError as err:
            await self.session.rollback()
            raise err
        else:
            return entity

    async def update(self, id: int, request: UpdateItemRequest):
        query = (
            update(Item)
            .values(
                {
                    "name": request.name,
                    "description": request.description,
                }
            )
            .where(Item.id == id)
        )
        query.execution_options(synchronize_session="fetch")
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise ItemNotFoundError(id)

    async def delete_by_id(self, id: int) -> None:
        query = delete(Item).where(Item.id == id)
        query.execution_options(synchronize_session="fetch")
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise ItemNotFoundError(id)


class NotFoundError(NoResultFound):
    entity_name: str

    def __init__(self, id):
        super().__init__(f"{self.entity_name} not found, id: {id}")


class ItemNotFoundError(NotFoundError):

    entity_name: str = "Item"
