from typing import AsyncGenerator, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import select, func, exists

from app.database.tables.currency import Currency, CurrencyLastUpdate
from app.schemas.currency import (
    CurrenciesList, CurrencyWithoutRate, LastCurrenctUpdate
)
from app.exceptions.errors import DoesNotExistsError, LastCurrenciesUpdateError


class CurrencyLastUpdateRepository:
    _model = CurrencyLastUpdate

    def __init__(self, session_factory: async_scoped_session) -> None:
        self.session_factory = session_factory

    async def update_or_create(self) -> None:
        async with self.session_factory() as session:
            query = select(self._model)
            last_currency_update = await session.execute(query.limit(1))
            last_currency_update_obj = last_currency_update.scalar_one_or_none()

            if not last_currency_update_obj:
                last_currency_update_obj = self._model(
                    last_update=datetime.now()
                )
            else:
                last_currency_update_obj.last_update = datetime.now()
            session.add(last_currency_update_obj)
            await session.commit()
        return None
    
    async def get_last_currency_update(self) -> LastCurrenctUpdate:
        async with self.session_factory() as session:
            query = select(self._model)
            last_currency_update = await session.execute(query.limit(1))
            last_currency_update_obj = last_currency_update.scalar_one_or_none()
            if not last_currency_update_obj:
                raise LastCurrenciesUpdateError        
            return LastCurrenctUpdate(
                last_update=last_currency_update_obj.last_update
            )


class CurrencyRepository:
    _model = Currency

    def __init__(self, session_factory: async_scoped_session) -> None:
        self.session_factory = session_factory
        
    async def create_currency(self, currency: CurrencyWithoutRate) -> None:
        currency = self._model(
            code=currency.code,
            title=currency.title, 
        )
        async with self.session_factory() as session, session.begin():
            session.add(currency)
            await session.flush()
        return None
    
    async def currency_exists(self, code: str) -> bool:
        async with self.session_factory() as session:
            currency = exists().where(self._model.code == code).select()
            result = await session.execute(currency)
            _exists = result.scalar()
            return bool(_exists)
    
    async def get_currency_by_code_and_update_rate(self, code: str, rate: float) -> None:
        async with self.session_factory() as session, session.begin():
            currency = await session.scalar(
                select(self._model).where(self._model.code == code)
            )
            currency.rate = rate
            session.add(currency)
            await session.commit()
        return None

    async def get_all_currencies(self) -> AsyncGenerator[CurrenciesList, Any]:
        async with self.session_factory() as session:
            stream = await session.stream_scalars(select(self._model).order_by(self._model.id))
            async for row in stream:
                yield CurrenciesList(
                    title=row.title,
                    code=row.code,
                    rate=row.rate, 
                )

    async def get_currency_rate(self, code) -> float:
        async with self.session_factory() as session:
            currency = await session.scalar(
                select(self._model).where(self._model.code == code)
            )
            
            if not currency:
                raise DoesNotExistsError
            return currency.rate
