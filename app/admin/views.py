from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.models import Rooms
from app.images.models import HotelImages
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.bookings]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    can_edit = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-book"


class HotelImagesAdmin(ModelView, model=HotelImages):
    column_list = [c.name for c in HotelImages.__table__.c] + [HotelImages.hotel]
    name = "Hotel's image"
    name_plural = "Hotel's images"
    icon = "fa-solid fa-image"
