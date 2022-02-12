from typing import Iterator
from app.data.repositories import ItemRepository
from app.models.entities.Item import Item
from app.models.requests.ItemRequest import AddItemRequest, UpdateItemRequest


class ItemService:
    def __init__(self, item_repository: ItemRepository) -> None:
        self._repository: ItemRepository = item_repository

    async def get_items(self) -> Iterator[Item]:
        return await self._repository.get_all()

    async def get_item_by_id(self, id: int) -> Item:
        return await self._repository.get(id)

    async def add_item(self, request: AddItemRequest) -> Item:
        return await self._repository.add(request)

    async def update_item(self, id: int, request: UpdateItemRequest) -> None:
        return await self._repository.update(id, request)

    async def delete_item_by_id(self, id: int) -> None:
        return await self._repository.delete_by_id(id)
