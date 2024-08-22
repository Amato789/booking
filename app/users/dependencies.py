from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from app.config import settings
from app.users.dao import UserDAO
from app.exceptions import (TokenAbsentException,
                            TokenExpiredException,
                            IncorrectTokenFormatException,
                            UserIsNotPresentException,
                            )


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
