from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    bookings = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"User {self.email}"