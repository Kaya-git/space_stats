from fastapi import APIRouter, Depends, Path


wb_api_router = APIRouter(
    prefix="/api/wb_api",
    tags=["Роутер для обращения к API WB"]
)

@wb_api_router.get("/get_cost_price")
async def get_cost_price():
    