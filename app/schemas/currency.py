from datetime import datetime

from pydantic import BaseModel


class CurrencyWithoutRate(BaseModel):
    code: str
    title: str


class CustomResp(BaseModel):
    message: str


class CurrenciesList(BaseModel):
    title: str
    code: str
    rate: float | None

    class Config:
        orm_mode = True


class CurrencyDB(BaseModel):
    title: str
    code: str
    rate: float

    class Config:
        orm_mode = True


class LastCurrenctUpdate(BaseModel):
    last_update: datetime

    class Config:
        orm_mode = True


class ConvertCurrencies(BaseModel):
    amount: float
    source_currency_code: str
    target_currency_code: str


class ConvertedCurrencyAmount(BaseModel):
    amount: float
