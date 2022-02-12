import pytest
from unittest import mock
from fastapi.testclient import TestClient
from app.main import app
from app.models.entities.Item import Item
from app.data.repositories.ItemRepository import ItemRepository, ItemNotFoundError
from app.models.requests.ItemRequest import AddItemRequest, UpdateItemRequest


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.get_all.return_value = [
        Item(id=1, name="Bath Towel", description="Blue"),
        Item(id=2, name="Hand Towel", description="Pink"),
    ]

    with app.container.item_repository.override(repository_mock):
        response = client.get("/items/all")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {
            "id": 1,
            "name": "Bath Towel",
            "description": "Blue",
        },
        {
            "id": 2,
            "name": "Hand Towel",
            "description": "Pink",
        },
    ]


def test_get_by_id(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.get.return_value = Item(id=1, name="Bath Towel", description="Blue")

    with app.container.item_repository.override(repository_mock):
        response = client.get("/items/get/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {
        "id": 1,
        "name": "Bath Towel",
        "description": "Blue",
    }
    repository_mock.get.assert_called_once_with(1)


def test_get_by_id_404(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.get.side_effect = ItemNotFoundError(1)

    with app.container.item_repository.override(repository_mock):
        response = client.get("/items/get/1")

    assert response.status_code == 404


def test_add(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.add.return_value = Item(id=1, name="Bath Towel", description="Blue")

    request = AddItemRequest(id=1, name="Bath Towel", description="Blue")
    with app.container.item_repository.override(repository_mock):
        response = client.post("/items/add", request.json())

    assert response.status_code == 201
    data = response.json()
    assert data == {
        "id": 1,
        "name": "Bath Towel",
        "description": "Blue",
    }
    repository_mock.add.assert_called_once_with(request)


def test_add_409(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.update.side_effect = ItemNotFoundError(1)

    request = AddItemRequest(id=1, name="Bath Towel", description="Red")
    with app.container.item_repository.override(repository_mock):
        response = client.put("/items/add", request.json())

    assert response.status_code == 409


def test_update(client):
    repository_mock = mock.Mock(spec=ItemRepository)

    request = UpdateItemRequest(name="Bath Towel", description="Red")
    with app.container.item_repository.override(repository_mock):
        response = client.put("/items/update/1", request.json())

    assert response.status_code == 200
    repository_mock.update.assert_called_once_with(1, request)


def test_update_404(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.update.side_effect = ItemNotFoundError(1)

    request = UpdateItemRequest(name="Bath Towel", description="Red")
    with app.container.item_repository.override(repository_mock):
        response = client.put("/items/update/999", request.json())

    assert response.status_code == 404


def test_delete(client):
    repository_mock = mock.Mock(spec=ItemRepository)

    with app.container.item_repository.override(repository_mock):
        response = client.delete("/items/delete/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


def test_delete_404(client):
    repository_mock = mock.Mock(spec=ItemRepository)
    repository_mock.delete_by_id.side_effect = ItemNotFoundError(1)

    with app.container.item_repository.override(repository_mock):
        response = client.delete("/items/delete/1")

    assert response.status_code == 404


def test_status(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "OK"}
