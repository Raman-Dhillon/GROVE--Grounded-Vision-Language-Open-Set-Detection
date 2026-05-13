from PIL import ImageDraw, ImageFont
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import torch

model_id = "IDEA-Research/grounding-dino-tiny"

processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id)

def detect_objects(image, prompt):
    image = image.convert("RGB")
    labels = [x.strip() for x in prompt.split(",") if x.strip()]
    if not labels:
        return image

    text = [f"a {label}" for label in labels]
    inputs = processor(images=image, text=[text], return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=0.15,
        text_threshold=0.15,
        target_sizes=[image.size[::-1]]
    )[0]

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("Arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    for box, label in zip(results["boxes"], results["labels"]):
        x1, y1, x2, y2 = [int(v) for v in box.tolist()]
        label_text = str(label).replace("a ", "")

        draw.rectangle([x1, y1, x2, y2], outline="green", width=4)

        bbox = draw.textbbox((x1, y1), label_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_y = max(0, y1 - text_h - 8)

        draw.rectangle([x1, text_y, x1 + text_w + 10, text_y + text_h + 6], fill="green")
        draw.text((x1 + 5, text_y + 2), label_text, fill="white", font=font)

    return image