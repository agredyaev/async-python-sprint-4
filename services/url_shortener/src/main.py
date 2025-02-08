import uvicorn

from api import setup_routers
from conf.exceptions import register_exception_handlers
from conf.settings import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logging import CoreLogger

CoreLogger.setup()

app = FastAPI(
    root_path=settings.app.root_path,
    title=settings.app.name,
    default_response_class=ORJSONResponse,
    docs_url=settings.api.docs_url,
    openapi_url=settings.api.openapi_url,
)


register_exception_handlers(app=app)
setup_routers(app=app)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app.host, port=settings.app.port)
