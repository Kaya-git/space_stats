from fastapi import FastAPI
import logging


LOGGER = logging.getLogger(__name__)


wb_api = FastAPI(
    title="WB_API"
)


async def root():
    ...


@wb_api.on_event("startup")
async def on_startup():
    LOGGER.info("--- Start up App ---")


@wb_api.on_event
async def shutdown():
    LOGGER.info("--- Shudown App ---")
