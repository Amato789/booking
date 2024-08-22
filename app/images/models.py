from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class HotelImages(Base):
    __tablename__ = "hotelimages"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    hotel: Mapped["Hotels"] = relationship(back_populates="images")

    def __str__(self):
        return self.name
