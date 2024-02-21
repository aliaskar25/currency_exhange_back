from dependency_injector import containers, providers

from app.config import settings
from app.database.database import Database

from app.repositories.currency_repository import (
    CurrencyRepository, CurrencyLastUpdateRepository
)
from app.services.currency_service import CurrencyService
from app.api_client.get_currency_data import CurrencyExchangeratesAPIClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.DATABASE_URL)

    currency_repository = providers.Factory(
        CurrencyRepository, session_factory=db.provided.session
    )

    currency_last_update_repository = providers.Factory(
        CurrencyLastUpdateRepository, session_factory=db.provided.session
    )

    currency_exchangerates_api_client = providers.Factory(
        CurrencyExchangeratesAPIClient
    )

    currency_service = providers.Factory(
        CurrencyService,
        currency_repository=currency_repository, 
        currency_last_update_repository=currency_last_update_repository,
        currency_exchangerates_api_client=currency_exchangerates_api_client, 
    )


container = Container()
container.config.from_pydantic_settings(settings)