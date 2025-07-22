import fitz  # PyMuPDF
import os
import json
from PIL import Image

def extract_content(pdf_path, output_dir):
    os.makedirs(f"{output_dir}/images", exist_ok=True)

    doc = fitz.open(pdf_path)
    content = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        images = []

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_num+1}_image{img_index+1}.{image_ext}"
            image_path = os.path.join(output_dir, "images", image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            images.append(image_path)

        content.append({
            "page": page_num + 1,
            "text": text.strip(),
            "images": images
        })

    return content