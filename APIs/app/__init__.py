from fastapi import FastAPI

from .api import init_app
from .settings import Settings


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI()
    init_app(app)
    return app
