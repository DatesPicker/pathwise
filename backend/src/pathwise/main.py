import logging

from fastapi import FastAPI

from pathwise.api.router import api_router
from pathwise.core.config import get_settings
from pathwise.core.logging import configure_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    app = FastAPI(title=settings.app_name)
    app.include_router(api_router)
    logger.info(
        "application_configured",
        extra={"environment": settings.environment},
    )
    return app


app = create_app()
