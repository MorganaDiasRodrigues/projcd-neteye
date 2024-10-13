from fastapi import APIRouter, Depends, FastAPI
from .routes import router as routes_router


def init_app(app: FastAPI) -> None:
    router = get_router()
    app.include_router(router)


def get_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(
        routes_router,
    )
    return api_router
