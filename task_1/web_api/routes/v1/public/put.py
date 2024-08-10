from http import HTTPStatus
from fastapi import Request

from shared.db.redis import Redis
from web_api.exceptions import NotFoundException
from web_api.exceptions.base import ExceptionResponseSchema
from .router import router as put_router
from pydantic import BaseModel, ConfigDict


class RouteResponse(BaseModel):
    phone: str
    address: str


class RequestBody(BaseModel):
    model_config = ConfigDict(extra='forbid')

    phone: str
    address: str


@put_router.put(
    "/write_data",
    response_model=RouteResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def change_address(request: Request, body: RequestBody):
    r_client: Redis = request.app.state.r_client
    existing_address = await r_client.get(body.phone)
    if not existing_address:
        raise NotFoundException
    await r_client.insert(
        key=body.phone,
        value=body.address
    )
    return RouteResponse(
        phone=body.phone,
        address=body.address
    )
