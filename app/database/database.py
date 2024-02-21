import logging
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.config import POSTGRES_URL

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.async_engine = create_async_engine(
            POSTGRES_URL,
            pool_pre_ping=True,
        )
        self.session_factory = async_scoped_session(
            async_sessionmaker(
                self.async_engine,
                expire_on_commit=False,
                autoflush=False,
                future=True,
            ),
            scopefunc=current_task,
        )
        async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            autoflush=False,
            future=True,
        )

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except IntegrityError as exception:
            logger.error("Session rollback because of exception: %s", exception)
            await session.rollback()
        finally:
            await session.close()
