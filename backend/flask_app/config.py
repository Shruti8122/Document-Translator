import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
FRONTEND_FOLDER = os.path.join(BASE_DIR, "..", "..", "frontend", "dist")
FASTAPI_URL = "http://localhost:8000"
SECRET_KEY = "doc-translator-secret-key-change-in-production"
MAX_CONTENT_LENGTH = 50 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf"}
