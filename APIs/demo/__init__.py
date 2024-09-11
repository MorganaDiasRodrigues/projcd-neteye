from fastapi import FastAPI

from . import api, health
from .dependencies import cors, lifespan


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    cors.setup(app)
    api.init_app(app)
    health.init_app(app)

    return app
