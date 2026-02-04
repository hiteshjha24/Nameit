from transformers.models.blip import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from utils import load_image_safely

print("Loading vision model...")

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def get_image_caption(image_path):
    image = load_image_safely(image_path)
    if image is None:
        return "Image not ready"
    inputs = processor(images=image, return_tensors="pt").to(device)

    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return caption