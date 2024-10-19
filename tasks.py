from celery import shared_task
from models.log import Log
from init import create_app
from flask_sqlalchemy import SQLAlchemy
from tele import send_image
import asyncio

app = create_app()
celery_app = app.extensions["celery"]
db=SQLAlchemy(app)

@shared_task(ignore_result=True)
def log_task(action, image_id):
    try:
        log_entry = Log(
            action=action,
            image_id=image_id,
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    except Exception as e:
        print(str(e))
        return None


@shared_task(ignore_result=True)
def log_to_csv(scan_time, abs_path):
    try:
        with open("/usr/src/app/log.csv", "r+") as f:
            length = len(f.readlines())
            print(length)
            f.write(f"{length+1},{scan_time},{abs_path}\n")
        return True
    except Exception as e:
        print(str(e))
        return None


@shared_task(ignore_result=True)
def send_image_to_telegram(img_path):
    print(img_path)
    try:
        print(img_path)
        asyncio.run(send_image("/usr/src/app/images/" + img_path.split("/")[-1]))
        return True
    except Exception as e:
        print(str(e))
        return None
