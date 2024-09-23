from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "The user already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "The token has expired"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "The token is missing"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomFullyBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "There are no rooms left"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Failed to book a room due to an unknown error"


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The check-in date cannot be later than the check-out date"


class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Unable to book a hotel for more than one month"


class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to add a record"


class CannotProcessCSV(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to process CSV file"
