from fastapi import FastAPI

from app.admin.auth import authentication_backend
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from fastapi.staticfiles import StaticFiles

from app.pages.router import router as router_pages

from fastapi.middleware.cors import CORSMiddleware

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from app.config import settings

from sqladmin import Admin
from app.database import engine
from app.admin.views import UsersAdmin, HotelsAdmin, BookingsAdmin, RoomsAdmin, HotelImagesAdmin


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8",
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title='Booking service',
    root_path="/api",
    description='Booking service description',
    debug=True,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)


admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelImagesAdmin)


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)


