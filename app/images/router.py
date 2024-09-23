from uuid import uuid4

from fastapi import APIRouter, UploadFile
from PIL import Image

from app.exceptions import CannotAddDataToDatabase
from app.images.dao import HotelImagesDAO

router = APIRouter(
    prefix="/images",
    tags=["Download images"],
)


@router.post("/hotels")
async def add_hotel_image(hotel_id: int, file: UploadFile):
    file_name = f"resized_1024_768_{str(uuid4())}.webp"

    image = await HotelImagesDAO.add(hotel_id=hotel_id, image_name=file_name)
    if not image:
        raise CannotAddDataToDatabase

    im = Image.open(file.file)
    im_resized_1024_768 = im.resize((1024, 768))
    im_resized_1024_768.save(f"app/static/images/{file_name}")
