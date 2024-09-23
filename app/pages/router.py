from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.bookings.router import get_bookings
from app.hotels.router import get_hotels_by_location_and_date
from app.utils import format_number_thousand_separator

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_hotels_by_location_and_date)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(
        name="auth/login.html",
        context={"request": request}
    )


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse(
        name="auth/register.html",
        context={"request": request}
    )


# @router.post("/successful_booking", response_class=HTMLResponse)
# async def get_successful_booking_page(
#         request: Request,
#         _=Depends(get_bookings),
# ):
#     return templates.TemplateResponse(
#         "bookings/booking_successful.html", {"request": request}
#     )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
    request: Request,
    bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
