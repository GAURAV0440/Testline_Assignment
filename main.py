import time
import json
import os
from backend.extractor import extract_content
from backend.question_generator import generate_question_from_image

pdf_path = "input/sample.pdf"
output_dir = "output"

# Step 1: Extract content
raw_data = extract_content(pdf_path, output_dir)

# Step 2: AI-based question generation
final_data = []

for page in raw_data:
    # Filter out small watermark-like images
    images = [img for img in page["images"] if os.path.getsize(img) > 5000]

    if images:
        question = generate_question_from_image(images[0])
        time.sleep(5)  # avoid hitting Gemini quota
    else:
        question = page["text"] if page["text"] else "Could not generate question."

    final_data.append({
        "question": question,
        "images": images[0] if images else "",
        "option_images": images[1:] if len(images) > 1 else []
    })

# Step 3: Save structured output
json_path = os.path.join(output_dir, "data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print("✅ Final structured JSON saved to:", json_path)
