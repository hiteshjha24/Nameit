import time
import os
import watchdog
from watchdog.observers import Observer
from vision import get_image_caption
from watchdog.events import FileSystemEventHandler
from ocr import extract_text
from namer import generate_filename

SCREENSHOT_FOLDER = r"C:\Users\Lenovo\OneDrive\Pictures\Screenshots"

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        file_name = os.path.basename(file_path)

        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"New screenshot detected: {file_name}")

            caption = get_image_caption(file_path)
            print(f"AI Caption: {caption}")

            ocr_text = extract_text(file_path)
            print(f"OCR Text: {ocr_text}")

            name = generate_filename(caption, ocr_text)
            print(f"AI Filename: {name}")


if __name__ == "__main__":
    print("Waiting for screenshot...")

    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, SCREENSHOT_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped monitoring.")

    observer.join()