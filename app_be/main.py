# Third party modules
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

# Local modules
from config.setup import config
from tools.custom_logging import create_unified_logger
from routes.base import router as base_router
from routes.product_routes import router as products_router


class Service(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level, self.logger = create_unified_logger(log_level=config.log_level)

@asynccontextmanager
async def lifespan(service: Service):
    await startup(service)
    yield
    await shutdown(service)


app = Service(lifespan=lifespan, title=config.app_name)
app.include_router(base_router)
app.include_router(products_router)


async def startup(service: Service):
    service.logger.info(f"{config.app_name.upper()} | Starting up ...")

# ---------------------------------------------------------
#
async def shutdown(service: Service):
    service.logger.info(f"{config.app_name.upper()} | Shutting down ...")



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
