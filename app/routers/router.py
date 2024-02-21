from fastapi import APIRouter

from app.routers.v1.currency import currency_router

router = APIRouter(tags=['API'], prefix='/api')

router.include_router(currency_router, tags=['currency'])
