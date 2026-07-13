import os
import json
import threading
import requests
from . import config
from .pdf_utils import pdf_to_images, read_image_bytes, text_to_pdf

tasks = {}
_lock = threading.Lock()


def get_progress(task_id: str):
    with _lock:
        return tasks.get(task_id)


def _update(task_id: str, progress: int, message: str, error: str = None):
    with _lock:
        tasks[task_id] = {
            "progress": progress,
            "message": message,
            "error": error,
        }


def run_translation(task_id: str, pdf_path: str, source_lang: str, target_lang: str):
    try:
        task_dir = os.path.join(config.UPLOAD_FOLDER, task_id)
        images_dir = os.path.join(task_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        _update(task_id, 5, "Converting PDF to images...")

        image_paths = pdf_to_images(pdf_path, images_dir)
        total_pages = len(image_paths)
        if total_pages == 0:
            _update(task_id, 0, "Error", error="PDF has no pages")
            return

        ocr_texts = []
        for i, img_path in enumerate(image_paths):
            pct = 10 + int((i / total_pages) * 40)
            _update(task_id, pct, f"Running OCR on page {i + 1}/{total_pages}...")

            img_bytes = read_image_bytes(img_path)
            resp = requests.post(
                f"{config.FASTAPI_URL}/api/ocr",
                files={"file": ("page.png", img_bytes, "image/png")},
                params={"source_lang": source_lang},
                timeout=300,
            )
            if resp.status_code != 200:
                _update(task_id, 0, "Error", error=f"OCR failed on page {i + 1}: {resp.text}")
                return
            ocr_texts.append(resp.json()["text"])

        translated_texts = []
        for i, text in enumerate(ocr_texts):
            if not text.strip():
                translated_texts.append("")
                continue
            pct = 50 + int((i / total_pages) * 40)
            _update(task_id, pct, f"Translating page {i + 1}/{total_pages}...")

            resp = requests.post(
                f"{config.FASTAPI_URL}/api/translate",
                json={"text": text, "target_lang": target_lang},
                timeout=300,
            )
            if resp.status_code != 200:
                _update(task_id, 0, "Error", error=f"Translation failed on page {i + 1}: {resp.text}")
                return
            translated_texts.append(resp.json()["translated_text"])

        _update(task_id, 92, "Generating translated PDF...")

        output_pdf = os.path.join(task_dir, "output.pdf")
        target_script = target_lang.split("_")[1] if "_" in target_lang else "Latn"
        text_to_pdf(translated_texts, output_pdf, target_script)

        _update(task_id, 100, "Translation complete!")

    except Exception as e:
        _update(task_id, 0, "Error", error=str(e))
