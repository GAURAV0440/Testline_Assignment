# 📄 AI-Based PDF Question Extractor

This project extracts questions and images from educational PDFs and uses AI to generate multiple-choice questions based on visual content.

---
## 🧰 Tech Stack

- Python
- Streamlit
- PyMuPDF (for PDF parsing)
- Pillow
- Gemini 1.5 Flash (via Google Generative AI API)
- `python-dotenv` for secure API key loading

---

## 📂 Folder Structure

ai_pdf_processor/
├── app/
│ └── ui.py # Streamlit UI
├── backend/
│ ├── extractor.py # PDF parser
│ └── question_generator.py # Gemini-based question generator
├── input/ # Upload PDF here
├── output/
│ ├── images/ # Extracted image files
│ └── data.json # Final structured result
├── main.py # CLI runner (optional)
├── requirements.txt
├── .env # Store GEMINI_API_KEY here


---

## ▶️ How to Run

### 1. Clone repo & install requirements

```bash
pip install -r requirements.txt
```

2. Add .env file
env
GEMINI_API_KEY=your_key_here

3. Launch the app
streamlit run app/ui.py
