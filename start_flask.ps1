Write-Host "Starting Flask Web Server..." -ForegroundColor Cyan
conda activate Doc_Translator
python -m backend.flask_app.app
