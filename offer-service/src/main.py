from fastapi import FastAPI
import logging
import pika
from config import conf

app = FastAPI(
    title="offer-service"
)

LOGGER = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    LOGGER.info("--- Start up App ---")
    conf.rbtmq.build_connection()


@app.on_event
async def shutdown():
    LOGGER.info("--- Shudown App ---")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)
