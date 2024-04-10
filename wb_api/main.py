from fastapi import FastAPI
import logging
from statistics_client import StatisticsApiClient
from standart_client import StandardApiClient


LOGGER = logging.getLogger(__name__)


wb_api = FastAPI(
    title="WB_API"
)


async def main():
    ...


@wb_api.on_event("startup")
async def on_startup():
    LOGGER.info("--- Start up App ---")


@wb_api.on_event
async def shutdown():
    LOGGER.info("--- Shudown App ---")
