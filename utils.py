import time
from PIL import Image

def load_image_safely(path, retries=10, delay=0.5):
    for _ in range(retries):
        try:
            img = Image.open(path).convert("RGB")
            return img
        except PermissionError:
            time.sleep(delay)
    return None