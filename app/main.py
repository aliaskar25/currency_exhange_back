from fastapi import FastAPI

from app import setup
from app.config import settings
from app.containers import container

app_container_modules = [
    "app.routers.v1.currency",
]


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE, docs_url="/api/docs/ui", debug=settings.DEBUG
    )
    container.wire(app_container_modules)

    setup.setup_routes(app)
    return app
