import re
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

print("Loading naming model...")

model_name = "google/flan-t5-small"

tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def generate_filename(caption, ocr_text):
    text = (
        "Create a 4-word filename. Use both sources if possible.\n"
        f"Caption: {caption}\n"
        f"Text: {ocr_text}\n"
        "Return only the filename words."
    )

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=12,
        num_beams=4,
        no_repeat_ngram_size=2
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    result = result.lower().strip()

    def sanitize(s):
        s = s.lower()
        s = re.sub(r"[^a-z0-9]+", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        if not s:
            return ""
        return "_".join(s.split()[:6])[:50]

    cleaned = sanitize(result)
    if cleaned in {"", "caption", "image", "screenshot"}:
        fallback = sanitize(f"{caption} {ocr_text}")
        return fallback if fallback else "screenshot_image"

    return cleaned if cleaned else "screenshot_image"
