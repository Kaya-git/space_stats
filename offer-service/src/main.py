from fastapi import FastAPI
import logging
from config import conf

app = FastAPI(
    title="offer-service"
)

LOGGER = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    LOGGER.info("--- Start up App ---")
    conf.rbtmq.build_connection()
    rbtmq_channel = conf.rbtmq.get_channel()
    rbtmq_channel.exchange_declare(
        exchange="offer_service",
        exchange_type="fanout"
    )


@app.on_event
async def shutdown():
    LOGGER.info("--- Shudown App ---")
    conf.rbtmq.close_connection()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)
