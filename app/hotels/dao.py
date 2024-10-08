from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels, Rooms
from app.images.models import HotelImages


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        """
        with booked_rooms as (
            select room_id, COUNT(room_id) as qty_booked from bookings
            where
                (date_from >= '2023-06-15' and date_to <= '2023-06-30') or
                (date_from <= '2023-06-15' and date_to > '2023-06-15')
            group by room_id
        ), booked_rooms_extended as (
            select
                booked_rooms.*,
                rooms.hotel_id,
                rooms.quantity,
                rooms.quantity - booked_rooms.qty_booked as qty_free_rooms
            from booked_rooms
            left join rooms on rooms.id = booked_rooms.room_id
        )
        select hotels.id, SUM(coalesce(qty_free_rooms, rooms.quantity))
        as rooms_available   from rooms
        left join booked_rooms_extended on booked_rooms_extended.room_id = rooms.id
        left join hotels on hotels.id = rooms.hotel_id
        where qty_free_rooms > 0 or booked_rooms_extended.room_id is null
        group by hotels.id
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Bookings.room_id, func.count(Bookings.room_id).label("qty_booked")
                )
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_to <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    )
                )
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )

            booked_rooms_extended = (
                select(
                    booked_rooms,
                    Rooms,
                    (Rooms.quantity - booked_rooms.c.qty_booked).label(
                        "qty_free_rooms"
                    ),
                )
                .select_from(booked_rooms)
                .join(Rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                .cte("booked_rooms_extended")
            )

            rooms_available = (
                select(
                    Hotels.__table__.columns,
                    func.min(HotelImages.name).label("images"),
                    func.sum(
                        func.coalesce(
                            booked_rooms_extended.c.qty_free_rooms, Rooms.quantity
                        )
                    ).label("rooms_available"),
                )
                .select_from(Rooms)
                .join(
                    booked_rooms_extended,
                    booked_rooms_extended.c.room_id == Rooms.id,
                    isouter=True,
                )
                .join(Hotels, Hotels.id == Rooms.hotel_id, isouter=True)
                .join(HotelImages, HotelImages.hotel_id == Rooms.hotel_id, isouter=True)
                .where(
                    and_(
                        or_(
                            booked_rooms_extended.c.qty_free_rooms > 0,
                            booked_rooms_extended.c.room_id == None,
                        ),
                        Hotels.location.ilike(f"%{location}%"),
                    )
                )
                .group_by(Hotels.id)
            )

            rooms_available = await session.execute(rooms_available)
            rooms_available = rooms_available.mappings().all()
            return rooms_available

    @classmethod
    async def find_by_id(cls, model_id):
        """
        select hotels.id , hotels.name, hotelimages.name from hotels
        left join hotelimages on hotelimages.hotel_id=hotels.id
        where hotels.id=1 limit 1;
        """
        async with async_session_maker() as session:
            query = (
                select(
                    Hotels.__table__.columns,
                    func.coalesce(HotelImages.name, "").label("images"),
                )
                .join(HotelImages, HotelImages.hotel_id == Hotels.id, isouter=True)
                .where(Hotels.id == model_id)
                .limit(1)
            )
            result = await session.execute(query)
            return result.mappings().all()


class RoomDAO(BaseDAO):
    model = Rooms
