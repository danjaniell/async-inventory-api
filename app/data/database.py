import logging
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session

logger = logging.getLogger(__name__)


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True, future=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def session(self) -> AsyncIterator[AsyncSession]:
        async_session = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )
        try:
            async with async_session() as session:
                yield session
        except Exception:
            logger.exception("Session rollback because of exception.")
            session.rollback()
            raise
        finally:
            session.close()
