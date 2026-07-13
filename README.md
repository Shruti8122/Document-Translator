# Doc Translator

Document translation web app using **EasyOCR** for OCR and **NLLB-200** for translation.

## Architecture

- **FastAPI** (port 8000) — Model inference service: OCR and translation
- **Flask** (port 5000) — Web server: file upload, progress tracking, result delivery
- **React + Vite** (port 3000 dev) — Glassmorphism frontend

## Quick Start

### 1. Conda Environment

```bash
conda env create -f environment.yaml
conda activate Doc_Translator
```

### 2. Frontend

```bash
cd frontend
npm install
npm run build    # production build served by Flask
# OR for development:
npm run dev      # starts on port 3000 with proxy to Flask
```

### 3. Start Services

Open **3 terminals** (all must have `conda activate Doc_Translator`):

| Terminal | Command | Port |
|----------|---------|------|
| 1 (FastAPI) | `uvicorn backend.fastapi_app.main:app --host 0.0.0.0 --port 8000` | 8000 |
| 2 (Flask) | `python -m backend.flask_app.app` | 5000 |
| 3 (Frontend dev) | `cd frontend && npm run dev` | 3000 |

Or use the PowerShell scripts:
```powershell
.\start_fastapi.ps1
.\start_flask.ps1
.\start_frontend.ps1
```

### 4. Open

Navigate to **http://localhost:3000** (dev) or **http://localhost:5000** (production).

## Notes

- First run loads EasyOCR + NLLB models from HuggingFace (~2GB download).
- CUDA GPU is recommended. Falls back to CPU if unavailable.
- Supported languages: English, Hindi, French, Spanish, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Bengali, Turkish, Vietnamese, Thai, Dutch, Polish, Romanian, Swedish, Czech, Greek, Hungarian, Indonesian, Malay, Ukrainian, Hebrew, Urdu, Tamil, Telugu.
