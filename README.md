# 🌍 AI Document Translator

An AI-powered document translation web application that extracts text from PDF documents using **EasyOCR**, translates the extracted text into multiple languages using **Meta's NLLB-200 (No Language Left Behind)** model, and generates a translated PDF for download.

The project features a modern React frontend with a Flask/FastAPI backend, providing a simple and intuitive workflow for document translation.

---

## ✨ Features

- 📄 Upload PDF documents
- 🔍 Extract text using EasyOCR
- 🌐 Translate text into multiple languages using NLLB-200
- 📊 Live translation progress tracking
- 👀 Preview translated PDF inside the application
- 📥 Download translated PDF
- 🎨 Modern glassmorphism user interface
- ⚡ Responsive and user-friendly frontend

---

## 🖥️ Tech Stack

### Frontend
- React.js
- Vite
- React Router
- Axios
- React Dropzone
- Framer Motion
- React Icons
- CSS (Glassmorphism UI)

### Backend
- Python
- Flask
- FastAPI
- EasyOCR
- Transformers (Hugging Face)
- PyTorch
- PyMuPDF
- ReportLab

---

## 📂 Project Structure

```
Doc_Translator/
│
├── backend/
│   ├── flask_app/
│   ├── fastapi_app/
│   └── uploads/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── EasyOCR/
├── environment.yaml
├── README.md
└── requirements.txt
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shruti8122/Document-Translator.git
cd Document-Translator
```

---

### 2. Create the Conda environment

```bash
conda env create -f environment.yaml
```

Activate it

```bash
conda activate Doc_Translator
```

---

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## ▶️ Running the Project

### Start Flask Backend

```bash
cd backend/flask_app
python app.py
```

or

```bash
flask run
```

---

### Start FastAPI Backend (Optional)

```bash
cd backend/fastapi_app
uvicorn main:app --reload
```

---

### Start React Frontend

```bash
cd frontend
npm run dev
```

The application will be available at

```
http://localhost:5173
```

---

## 📖 Workflow

1. Upload a PDF document.
2. Select the source language.
3. Select the target language.
4. Start translation.
5. Monitor translation progress.
6. Preview translated PDF.
7. Download translated document.

---

## 📷 Screenshots

You can add screenshots here after uploading them.

### Home Page

```
screenshots/home.png
```

### Language Selection

```
screenshots/language.png
```

### Translation Progress

```
screenshots/progress.png
```

### Result Page

```
screenshots/result.png
```

---

## 📦 Main Python Libraries

- EasyOCR
- Transformers
- Torch
- Flask
- FastAPI
- Uvicorn
- PyMuPDF
- Pillow
- ReportLab
- SentencePiece
- NumPy

---

## 📌 Future Improvements

- Support DOCX input
- Support image input
- Batch document translation
- Translation history
- User authentication
- Cloud deployment
- OCR confidence visualization
- Multiple translation models

---

## 👩‍💻 Author

**Shruti Singh**

B.Tech CSE (Artificial Intelligence & Machine Learning)

GitHub: https://github.com/Shruti8122

---

## 🙏 Acknowledgements

- Meta AI for the NLLB-200 multilingual translation model.
- EasyOCR for optical character recognition.
- Hugging Face Transformers library.
- PyTorch team for the deep learning framework.
- React and Vite for the frontend ecosystem.

---

## 📄 License

This project is intended for educational and academic purposes.
