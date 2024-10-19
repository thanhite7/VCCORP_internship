from datetime import datetime

from flask import request, jsonify

from models.model import Image
from tasks import app, db
from tasks import log_task, log_to_csv, send_image_to_telegram


@app.route("/api/v1/get-all-images", methods=["GET"])
def get_all_images():
    try:
        images = db.session.query(Image).where(Image.is_deleted == False)
        for image in images:
            log_task.delay("read", image.id)
        return jsonify(
            {
                "images": [
                    {
                        "id": image.id,
                        "name": image.name,
                        "location": image.location,
                        "updated_at": image.updated_at,
                    }
                    for image in images
                ],
                "action": "read",
            }
        )
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/api/v1/add-image", methods=["POST"])
def add_images():
    try:
        images = dict(request.get_json())
        # print(images["name"], images["location"])
        db.session.add(
            Image(
                name=images["name"],
                location=images["location"],
                updated_at=datetime.now(),
                is_deleted=False,
            )
        )
        print(images["scan_time"], images["location"])
        log_to_csv.delay(images["scan_time"], images["location"])
        send_image_to_telegram.delay(images["location"])
        db.session.commit()
        new_image = db.session.query(Image).filter(Image.name == images["name"])
        for image in new_image:
            log_task.delay("create", image.id)

        return jsonify(
            {
                "message": "Image added successfully",
                "action": "create",
            }
        )
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/api/v1/change-images-info", methods=["PATCH"])
def change_images_info():
    try:
        new_image_info = request.get_json()
        db.session.query(Image).filter(
            Image.location == new_image_info["old_location"]
        ).update(
            {
                "is_deleted": True,
                "updated_at": datetime.now(),
            }
        )
        db.session.add(
            Image(
                name=new_image_info["new_location"].split("/")[-1],
                location=new_image_info["new_location"],
                updated_at=datetime.now(),
                is_deleted=False,
            )
        )
        modified_image = db.session.query(Image).filter(
            Image.location == new_image_info["new_location"]
        )
        db.session.commit()

        for image in modified_image:
            log_task.delay("update", image.id)

    
        return jsonify(
            {
                "message": "Image info changed successfully",
                "action": "update",
            }
        )
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/api/v1/delete-image", methods=["DELETE"])
def delete_image():
    try:
        image_path = request.get_json()["location"]
        deleted_image = db.session.query(Image).where(Image.location == image_path)
        for image in deleted_image:
            log_task.delay("delete", image.id)

        db.session.query(Image).filter(Image.location == image_path).update(
            {"is_deleted": True, "updated_at": datetime.now()}
        )
        db.session.commit()

        return jsonify(
            {
                "message": "Image deleted successfully",
                "action": "delete",
            }
        )
    except Exception as e:
        return jsonify({"message": str(e)})


if __name__ == "__main__":

    app.run(port=5000, debug=True)
