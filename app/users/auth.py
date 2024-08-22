from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from pydantic import EmailStr

from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UserDAO
from app.config import settings


pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_contex.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_contex.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not (user and verify_password(plain_password=password, hashed_password=user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user
