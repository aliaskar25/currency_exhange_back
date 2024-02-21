import aiohttp

from app.config import API_CLIENT_KEY
from app.exceptions.errors import BaseError


class CurrencyExchangeratesAPIClient:
    UPDATE_RATES_URL = f"http://api.exchangeratesapi.io/v1/latest?access_key={API_CLIENT_KEY}"
    UPDATE_CURRENCIES_URL = (
        f"http://api.exchangeratesapi.io/v1/symbols?access_key={API_CLIENT_KEY}"
    )
    ERRORS = {"missing_access_key": "No API Key was specified or an invalid API Key was specified"}

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    async def fetch_currencies_rates(self):
        async with aiohttp.ClientSession() as session:
            res = await self.fetch(session, self.UPDATE_RATES_URL)

            try:
                rates = res["rates"]
            except Exception:
                error_code = res["error"]["code"]
                error_message = self.ERRORS[error_code]
                raise BaseError(message=error_message, status_code=400)
        return rates

    async def fetch_all_currencies(self) -> dict:
        async with aiohttp.ClientSession() as session:
            res = await self.fetch(session, self.UPDATE_CURRENCIES_URL)
            try:
                symbols = res["symbols"]
            except Exception:
                error_code = res["error"]["code"]
                error_message = self.ERRORS[error_code]
                raise BaseError(message=error_message, status_code=400)
        return symbols
