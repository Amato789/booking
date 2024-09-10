from app.tasks.celery_setup import celery
from PIL import Image
from pathlib import Path


@celery.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1024_768 = im.resize((1024, 768))
    im_resized_800_600 = im.resize((800, 600))
    im_resized_1024_768.save(f"app/static/images/resized_1024_768_{im_path.name}")
    im_resized_800_600.save(f"app/static/images/resized_800_600_{im_path.name}")
