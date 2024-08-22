from app.dao.base import BaseDAO
from app.images.models import HotelImages
from app.hotels.models import Hotels
from app.database import async_session_maker
from sqlalchemy import select, and_, or_, func, insert, delete
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger


class HotelImagesDAO(BaseDAO):
    model = HotelImages

    @classmethod
    async def add(cls, hotel_id: int, image_name: str):
        try:
            async with async_session_maker() as session:
                hotel_query = select(Hotels).filter_by(id=hotel_id)
                hotel = await session.execute(hotel_query)
                hotel = hotel.scalars().first()

                if hotel:
                    add_image = insert(HotelImages).values(
                        hotel_id=hotel_id, name=image_name
                    ).returning(HotelImages.id)
                    new_image = await session.execute(add_image)
                    await session.commit()
                    return new_image.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "hotel_id": hotel_id,
                "name": image_name,
            }
            logger.error(msg, extra=extra, exc_info=True)
