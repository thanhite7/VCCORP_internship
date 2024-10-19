import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import os
from datetime import datetime
url = "http://127.0.0.1:5000"


class Watcher:
    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        if not event.is_directory:
            res = requests.post(
                f"{url}/api/v1/add-image",
                json={
                    "name": list(event.src_path.split("/"))[-1],
                    "location": event.src_path,
                    "scan_time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                },
            )
            print(f"File created: {event.src_path}")

    @staticmethod
    def on_created(event):
        if not event.is_directory:
            res = requests.post(
                f"{url}/api/v1/add-image",
                json={
                    "name": list(event.src_path.split("/"))[-1],
                    "location": event.src_path,
                    "scan_time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                },
            )
            print(f"File created: {event.src_path}")

    @staticmethod
    def on_moved(event):
        if not event.is_directory:
            res = requests.patch(
                f"{url}/api/v1/change-images-info",
                json={"old_location": event.src_path, "new_location": event.dest_path},
            )
            print(f"File renamed or moved: {event.src_path} -> {event.dest_path}")

    @staticmethod
    def on_deleted(event):
        if not event.is_directory:
            print(event.src_path)
            res = requests.delete(
                f"{url}/api/v1/delete-image", json={"location": event.src_path}
            )
            print(f"File deleted: {event.src_path}")


if __name__ == "__main__":
    directory_to_monitor = (
        "./images"
    )
    w = Watcher(directory_to_monitor)
    w.run()
