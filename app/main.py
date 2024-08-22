from fastapi import FastAPI
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from fastapi.staticfiles import StaticFiles

from app.pages.router import router as router_pages

app = FastAPI(
    title='Booking service',
    docs_url='/api/docs',
    description='Booking service description',
    debug=True,
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
