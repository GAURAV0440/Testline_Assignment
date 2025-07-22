import sys
import os
import uuid
import json
import time

import streamlit as st
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.extractor import extract_content
from backend.question_generator import generate_question_from_image

st.set_page_config(page_title="PDF to Question Extractor", layout="wide")
st.title("📄 PDF to Question Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Prevent re-processing on every rerun
if uploaded_file:
    if "processed" not in st.session_state or st.session_state.get("pdf_name") != uploaded_file.name:
        st.session_state.pdf_name = uploaded_file.name
        st.session_state.processed = True

        # Save uploaded file
        temp_filename = f"{uuid.uuid4()}.pdf"
        pdf_path = os.path.join("input", temp_filename)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("✅ PDF uploaded successfully!")

        # Extract content
        with st.spinner("🧠 Extracting and generating AI-based questions..."):
            result = extract_content(pdf_path, "output")

            final_data = []
            for page in result:
                images = [img for img in page["images"] if os.path.getsize(img) > 5000]

                if images:
                    ai_question = generate_question_from_image(images[0])
                    time.sleep(5)
                else:
                    ai_question = page["text"] if page["text"] else "Could not generate question."

                final_data.append({
                    "question": ai_question,
                    "images": images[0] if images else "",
                    "option_images": images[1:] if len(images) > 1 else []
                })

            # Save final JSON
            json_path = "output/data.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(final_data, f, indent=4)

        st.success("✅ All done! Preview below ⬇️")

        st.session_state.final_data = final_data
        st.session_state.json_path = json_path

# Render if data is already processed
if "final_data" in st.session_state:
    st.subheader("📋 AI-Generated Questions:")
    for i, item in enumerate(st.session_state.final_data, 1):
        st.markdown(f"### Question {i}")
        st.text(item["question"])
        if item["images"]:
            st.image(item["images"], caption="Question Image", width=300)
        for idx, opt_img in enumerate(item["option_images"]):
            st.image(opt_img, caption=f"Option {idx+1}", width=150)

    # Download button
    with open(st.session_state.json_path, "rb") as f:
        st.download_button("📥 Download JSON", f, file_name="data.json", mime="application/json")
