import schedule
import time as tm
from config import SCANPATH
from sqlalchemy import create_engine
import os
from models.model import Image
from app import app
import requests

url = "http://localhost:5000"
engine = create_engine("postgresql://thanhnt:thanhnt@localhost:5432/final_project")

before = [f for f in os.listdir(SCANPATH)]


def check_change_and_add_img():
    global before
    after = [f for f in os.listdir(SCANPATH)]
    added = [f for f in after if f not in before]
    removed = [f for f in before if f not in after]
    if added:
        for img in added:
            res = requests.post(
                f"{url}/add_image",
                json={"name": img, "location": os.path.join(SCANPATH, img)},
            )
            if res.status_code == 200:
                print("New image added")
            else:
                print("Failed to add new image")
    if removed:
        for img in removed:
            res = requests.delete(f"{url}/delete_image", json={"name": img})
            if res.status_code == 200:
                print("Image deleted")
            else:
                print("Failed to delete image")
    before = after


schedule.every(5).seconds.do(check_change_and_add_img)
while True:
    schedule.run_pending()
