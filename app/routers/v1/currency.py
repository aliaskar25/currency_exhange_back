from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.containers import Container

from app.services.currency_service import CurrencyService

from app.schemas.responses import CurrenciesListResponse
from app.schemas.currency import (
    LastCurrenctUpdate, ConvertCurrencies, 
    ConvertedCurrencyAmount
)


currency_router = APIRouter(prefix='/v1/currencies')


@currency_router.post('/')
@inject
async def update_currencies(
    currency_service: CurrencyService = Depends(Provide[Container.currency_service])
):
    try:
        await currency_service.create_currencies()
        return await currency_service.update_currencies()
    except Exception as error:
        raise HTTPException(status_code=400, detail=error.message)


@currency_router.get('/', response_model=CurrenciesListResponse)
@inject
async def get_currencies_list(
    currency_service: CurrencyService = Depends(Provide[Container.currency_service])
) -> CurrenciesListResponse:
    return CurrenciesListResponse(
        currencies=[
            currency async for currency in await currency_service.get_all_currencies()
        ]
    )


@currency_router.get('/last-update', response_model=LastCurrenctUpdate)
@inject
async def get_last_currency_update(
    currency_service: CurrencyService = Depends(Provide[Container.currency_service])
) -> LastCurrenctUpdate:
    try:
        return await currency_service.get_last_currency_update()
    except Exception as error:
        print(dir(error))
        print('-'*80)
        raise HTTPException(status_code=400, detail=error.message)


@currency_router.post('/convert-currencies')
@inject
async def convert_currencies(
    body: ConvertCurrencies, 
    currency_service: CurrencyService = Depends(Provide[Container.currency_service])
) -> ConvertedCurrencyAmount: 
    try:
        return await currency_service.convert_currencies(body)
    except Exception as error:
        raise HTTPException(status_code=404, detail=error.message)
