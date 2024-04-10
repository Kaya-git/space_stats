from fastapi import APIRouter, Path
from config import conf
import decimal


ItemCostPrice = decimal.Decimal


wb_api_router = APIRouter(
    prefix="/api/wb_api",
    tags=["Роутер для обращения к API WB"]
)


@wb_api_router.get("/get_cost_price")
async def get_cost_price(
    item: int,  # ВБ Артикул товара
    rpoff: decimal.Decimal,  # Себес готового товара на фул филе
    plw: decimal.Decimal,  # Стоимость логистики на единицу товара до склада ВБ
    pd: str  # Габариты Упаковки (д/ш/в)
) -> ItemCostPrice:

    rbtmq_channel = conf.rbtmq.get_channel()
    rbtmq_channel.basic_publish(
        exchange='',
        routing_key='cost_price',
        body='get_cost_price'
    )

    cost_price = rpoff + plw
