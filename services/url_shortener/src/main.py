import uvicorn

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from api import setup_routers
from conf.constraits import BLACKLIST, EXEMPT_ENDPOINTS
from conf.exceptions import register_exception_handlers
from conf.settings import settings
from core.logging import CoreLogger
from core.security import get_auth_service, setup_auth_middleware

CoreLogger.setup()

app = FastAPI(
    root_path=settings.app.root_path,
    title=settings.app.name,
    default_response_class=ORJSONResponse,
    docs_url=settings.api.docs_url,
    openapi_url=settings.api.openapi_url,
)

setup_auth_middleware(
    app=app,
    auth_service=Depends(get_auth_service),
    api_version=settings.api.version,
    exempt_endpoints=EXEMPT_ENDPOINTS,
    blacklist=BLACKLIST,
)
register_exception_handlers(app=app)
setup_routers(app=app)

if __name__ == "__main__":
    uvicorn.run(app=settings.app.app, host=settings.app.host, port=settings.app.port)
