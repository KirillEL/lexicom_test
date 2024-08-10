from shared.db.redis import Redis
from web_api.exceptions import NotFoundException
from web_api.exceptions.base import ExceptionResponseSchema
from .router import router as get_router
from pydantic import BaseModel
from fastapi import Request, Query


class RouteResponse(BaseModel):
    address: str


@get_router.get(
    "/check_data",
    response_model=RouteResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Получить адрес по ключу"
)
async def get_address_by_phone(request: Request, phone: str = Query(..., description="Номер телефона")):
    r_client: Redis = request.app.state.r_client
    address = await r_client.get(key=phone)
    if address is None:
        raise NotFoundException(message="Такого номера нет")
    return RouteResponse(
        address=address
    )
