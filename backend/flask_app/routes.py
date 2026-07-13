import os
import uuid
import threading
import requests
from flask import Blueprint, request, jsonify, send_file, render_template, send_from_directory
from . import config
from .tasks import get_progress, run_translation

api = Blueprint("api", __name__)


@api.route("/api/languages")
def get_languages():
    try:
        resp = requests.get(f"{config.FASTAPI_URL}/api/languages", timeout=5)
        return jsonify(resp.json())
    except requests.ConnectionError:
        return jsonify({"error": "FastAPI server not running"}), 503


@api.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "" or not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    task_id = str(uuid.uuid4())
    task_dir = os.path.join(config.UPLOAD_FOLDER, task_id)
    os.makedirs(task_dir, exist_ok=True)
    pdf_path = os.path.join(task_dir, "input.pdf")
    file.save(pdf_path)

    return jsonify({"task_id": task_id})


@api.route("/api/start-translation", methods=["POST"])
def start_translation():
    data = request.get_json()
    task_id = data.get("task_id")
    source_lang = data.get("source_lang", "en")
    target_lang = data.get("target_lang")

    if not task_id or not target_lang:
        return jsonify({"error": "task_id and target_lang are required"}), 400

    pdf_path = os.path.join(config.UPLOAD_FOLDER, task_id, "input.pdf")
    if not os.path.exists(pdf_path):
        return jsonify({"error": "Task not found"}), 404

    thread = threading.Thread(
        target=run_translation,
        args=(task_id, pdf_path, source_lang, target_lang),
        daemon=True,
    )
    thread.start()

    return jsonify({"task_id": task_id, "status": "started"})


@api.route("/api/progress/<task_id>")
def progress(task_id):
    status = get_progress(task_id)
    if status is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(status)


@api.route("/api/result/<task_id>")
def result(task_id):
    output_pdf = os.path.join(config.UPLOAD_FOLDER, task_id, "output.pdf")
    if not os.path.exists(output_pdf):
        return jsonify({"error": "Result not ready"}), 404
    return send_file(output_pdf, mimetype="application/pdf", as_attachment=False)


@api.route("/api/result/<task_id>/download")
def download_result(task_id):
    output_pdf = os.path.join(config.UPLOAD_FOLDER, task_id, "output.pdf")
    if not os.path.exists(output_pdf):
        return jsonify({"error": "Result not ready"}), 404
    return send_file(output_pdf, mimetype="application/pdf", as_attachment=True, download_name="translated_document.pdf")
