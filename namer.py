from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

print("Loading naming model...")

model_name = "google/flan-t5-small"

tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def generate_filename(caption, ocr_text):
    text = f"Create a short filename topic: Caption: {caption}. Text: {ocr_text}"

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)

    outputs = model.generate(
        **inputs,
        max_length=20
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    result = result.lower().replace(" ", "_")

    return result[:50] if result else "screenshot_image"
