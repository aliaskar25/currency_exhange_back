from pydantic import BaseModel

from .currency import CurrenciesList


class CurrenciesListResponse(BaseModel):
    currencies: list[CurrenciesList]
