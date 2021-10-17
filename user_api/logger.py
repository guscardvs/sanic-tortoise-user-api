import logging
from datetime import datetime

from sanic import HTTPResponse, Request, Sanic


def setup_logger(app: Sanic):
    logger = logging.getLogger(
        "{}.log".format("_".join(item.lower() for item in app.name.split()))
    )
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    app.ctx.logger = logger


def log_middleware_setup(app: Sanic):
    @app.on_response
    async def log_request(request: Request, response: HTTPResponse):
        logger: logging.Logger = request.app.ctx.logger
        logger.info(
            "[%s] - %s - %s - %s",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            response.status,
            request.method,
            request.path,
        )
