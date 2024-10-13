import uvicorn
from .settings import Settings


def main() -> None:
    settings = Settings()  # type: ignore
    uvicorn.run(
        app="app:create_app",
        factory=True,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
    )


if __name__ == "__main__":
    main()
