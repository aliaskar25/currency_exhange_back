from app.api_client.get_currency_data import CurrencyExchangeratesAPIClient
from app.repositories.currency_repository import (
    CurrencyLastUpdateRepository,
    CurrencyRepository,
)
from app.schemas.currency import (
    ConvertCurrencies,
    ConvertedCurrencyAmount,
    CurrencyWithoutRate,
    CustomResp,
    LastCurrenctUpdate,
)
from app.schemas.responses import CurrenciesListResponse


class CurrencyService:
    def __init__(
        self,
        *,
        currency_repository: CurrencyRepository,
        currency_last_update_repository: CurrencyLastUpdateRepository,
        currency_exchangerates_api_client: CurrencyExchangeratesAPIClient
    ) -> None:
        self._currency_repository = currency_repository
        self._currency_exchangerates_api_client = currency_exchangerates_api_client
        self._currency_last_update_repository = currency_last_update_repository

    async def create_currencies(self) -> None:
        try:
            currencies = (
                await self._currency_exchangerates_api_client.fetch_all_currencies()
            )
        except Exception as error:
            raise error

        for code, title in currencies.items():
            if await self._currency_repository.currency_exists(code):
                continue
            await self._currency_repository.create_currency(
                CurrencyWithoutRate(code=code, title=title)
            )
        return None

    async def update_currencies(self):
        try:
            currencies = (
                await self._currency_exchangerates_api_client.fetch_currencies_rates()
            )
        except Exception as error:
            raise error

        for code, rate in currencies.items():
            await self._currency_repository.get_currency_by_code_and_update_rate(
                code, rate
            )

        await self._currency_last_update_repository.update_or_create()
        return CustomResp(message="success")

    async def get_all_currencies(self) -> CurrenciesListResponse:
        return self._currency_repository.get_all_currencies()

    async def get_last_currency_update(self) -> LastCurrenctUpdate:
        try:
            return (
                await self._currency_last_update_repository.get_last_currency_update()
            )
        except Exception as error:
            raise error

    async def convert_currencies(
        self, body: ConvertCurrencies
    ) -> ConvertedCurrencyAmount:
        try:
            target_currency_rate = await self._currency_repository.get_currency_rate(
                body.target_currency_code
            )
            source_currency_rate = await self._currency_repository.get_currency_rate(
                body.source_currency_code
            )
        except Exception as error:
            raise error

        converted_amount = body.amount * float(
            target_currency_rate / source_currency_rate
        )
        return ConvertedCurrencyAmount(amount=converted_amount)
