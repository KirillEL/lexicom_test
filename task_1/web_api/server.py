from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from redis.asyncio import Redis
from starlette.responses import JSONResponse
from fastapi import Request

from shared.db.redis import run_redis
from web_api.exceptions.base import CustomException
from web_api.routes.v1 import main_router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(main_router)


def init_middlewares(app_: FastAPI) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message}
        )


@asynccontextmanager
async def lifespan(app_: FastAPI):
    app_.state.r_client: Redis = await run_redis()
    yield
    await app_.state.r_client.aclose()


def init_app() -> FastAPI:
    app_ = FastAPI(
        title="Lexicom test",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        lifespan=lifespan
    )
    init_middlewares(app_=app_)
    init_routers(app_=app_)
    init_listeners(app_=app_)

    return app_


app = init_app()
