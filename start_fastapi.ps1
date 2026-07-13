Write-Host "Starting FastAPI Inference Service..." -ForegroundColor Cyan
conda activate Doc_Translator
uvicorn backend.fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload
