from fastapi import APIRouter, Response, Depends
from app.users.schemas import UserAuthSchema
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register_user(user_data: UserAuthSchema):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(password=user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    # if not user:
    #     return IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_current_user(current_user: Users = Depends(get_current_user)):
    return current_user
