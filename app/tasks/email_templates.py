from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(
        f"""
        <h1>Booking confirmation.</h1>
        You are booked the hotel from {booking["date_from"]} to {booking["date_to"]}.
        """,
        subtype="html"
    )
    return email


def check_in_remainder_tomorrow_template(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Booking remainder"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(
        f"""
            <h1>Booking remainder.</h1>
            You are booked the hotel from {booking["date_from"]} to {booking["date_to"]}.
            """,
        subtype="html"
    )
    return email
