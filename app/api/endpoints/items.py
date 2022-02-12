from app.services.ItemsService import ItemService
from app.core.containers import Container
from app.data.repositories.ItemRepository import NotFoundError
from app.models.requests.ItemRequest import AddItemRequest, UpdateItemRequest
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import exc

router = APIRouter()


@router.get("/all")
@inject
async def get_all(
    item_service: ItemService = Depends(Provide[Container.item_service]),
):
    return await item_service.get_items()


@router.get("/get/{id}")
@inject
async def get(
    id: int,
    item_service: ItemService = Depends(Provide[Container.item_service]),
):
    try:
        return await item_service.get_item_by_id(id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=getattr(err, "message", repr(err)),
        )


@router.post("/add", status_code=status.HTTP_201_CREATED)
@inject
async def add(
    request: AddItemRequest,
    item_service: ItemService = Depends(Provide[Container.item_service]),
):
    try:
        return await item_service.add_item(request)
    except exc.IntegrityError as err:
        if "already exists" in getattr(err, "message", repr(err)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item already exists, id: {id}",
            )


@router.put("/update/{id}", status_code=status.HTTP_200_OK)
@inject
async def update(
    id: int,
    request: UpdateItemRequest,
    item_service: ItemService = Depends(Provide[Container.item_service]),
):
    try:
        await item_service.update_item(id, request)
    except NotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=getattr(err, "message", repr(err)),
        )
    else:
        return Response(status_code=status.HTTP_200_OK)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete(
    id: int,
    item_service: ItemService = Depends(Provide[Container.item_service]),
):
    try:
        await item_service.delete_item_by_id(id)
    except NotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=getattr(err, "message", repr(err)),
        )
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/")
async def get_status():
    return {"status": "OK"}
