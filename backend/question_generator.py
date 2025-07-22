import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Use updated Gemini Vision model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def generate_question_from_image(image_path):
    try:
        img = Image.open(image_path)
        prompt = "Look at this image and generate a short, clear multiple choice style question suitable for a 1st-grade math Olympiad."

        response = model.generate_content([prompt, img])

        if response and response.text:
            return response.text.strip()
        else:
            return "No meaningful question generated."

    except Exception as e:
        return f"Gemini error: {str(e)}"
