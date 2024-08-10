from starlette import status
from fastapi import Request

from shared.db.redis import Redis
from web_api.exceptions.base import ExceptionResponseSchema
from .router import router as post_router
from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    phone: str = Field(max_length=11, min_length=11)
    address: str = Field(min_length=1, max_length=255)


class Response(BaseModel):
    phone: str


@post_router.post(
    "/write_data",
    response_model=Response,
    status_code=status.HTTP_201_CREATED,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Записать в базу"
)
async def write_data_to_db(request: Request, body: RequestBody):
    r_client: Redis = request.app.state.r_client
    await r_client.insert(
        key=body.phone,
        value=body.address
    )
    return Response(
        phone=body.phone
    )
