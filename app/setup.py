from fastapi import FastAPI

from app.routers.router import router


def setup_routes(app: FastAPI) -> None:
    app.include_router(router)
