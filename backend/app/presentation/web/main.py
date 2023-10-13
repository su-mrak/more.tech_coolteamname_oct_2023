from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from presentation.web.router import router
from shared.settings import app_settings


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)

    @app.on_event("startup")
    async def startup() -> None:
        redis = aioredis.from_url(
            f"redis://{app_settings.redis_host}:{app_settings.redis_port}"
        )
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    return app
