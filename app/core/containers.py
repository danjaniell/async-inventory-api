from dependency_injector import containers, providers
from app.data.database import Database
from app.data.repositories.ItemRepository import ItemRepository
from app.services.ItemsService import ItemService
from .config import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.items",
        ]
    )

    db = providers.Singleton(Database, db_url=settings.DATABASE_URI)

    item_repository = providers.Factory(
        ItemRepository,
        session=providers.Resource(db.provided.session()),
    )

    item_service = providers.Factory(
        ItemService,
        item_repository=item_repository,
    )
