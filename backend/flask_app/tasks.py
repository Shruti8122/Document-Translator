import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from . import config
from .pdf_utils import pdf_to_images, read_image_bytes, text_to_pdf
from ..fastapi_app.ocr_engine import ocr_image
from ..fastapi_app.translator import translate_text
from ..fastapi_app.config import LANGUAGE_MAP

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


def _ocr_single(img_path, source_lang):
    img_bytes = read_image_bytes(img_path)
    ocr_langs = [source_lang]
    if source_lang != "en":
        ocr_langs.append("en")
    return ocr_image(img_bytes, ocr_langs)


def _translate_single(text, target_lang):
    if not text.strip():
        return ""
    return translate_text(text, target_lang)


def run_translation(task_id: str, pdf_path: str, source_lang: str, target_lang: str):
    try:
        for v in LANGUAGE_MAP.values():
            if v["nllb"] == source_lang:
                source_lang = v["easyocr"]
                break
        easyocr_codes = {v["easyocr"] for v in LANGUAGE_MAP.values()}
        if source_lang not in easyocr_codes:
            source_lang = "en"

        task_dir = os.path.join(config.UPLOAD_FOLDER, task_id)
        images_dir = os.path.join(task_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        _update(task_id, 5, "Converting PDF to images...")

        image_paths = pdf_to_images(pdf_path, images_dir)
        total_pages = len(image_paths)
        if total_pages == 0:
            _update(task_id, 0, "Error", error="PDF has no pages")
            return

        ocr_texts = [None] * total_pages
        _update(task_id, 10, f"Running OCR on {total_pages} pages (parallel)...")
        with ThreadPoolExecutor(max_workers=4) as executor:
            fut_map = {executor.submit(_ocr_single, img_path, source_lang): i
                       for i, img_path in enumerate(image_paths)}
            for fut in as_completed(fut_map):
                idx = fut_map[fut]
                ocr_texts[idx] = fut.result()
                done = sum(1 for t in ocr_texts if t is not None)
                pct = 10 + int((done / total_pages) * 40)
                _update(task_id, pct, f"OCR: {done}/{total_pages} pages done...")

        translated_texts = [None] * total_pages
        _update(task_id, 50, f"Translating {total_pages} pages (parallel)...")
        with ThreadPoolExecutor(max_workers=4) as executor:
            fut_map = {executor.submit(_translate_single, text, target_lang): i
                       for i, text in enumerate(ocr_texts)}
            for fut in as_completed(fut_map):
                idx = fut_map[fut]
                translated_texts[idx] = fut.result()
                done = sum(1 for t in translated_texts if t is not None)
                pct = 50 + int((done / total_pages) * 40)
                _update(task_id, pct, f"Translate: {done}/{total_pages} pages done...")

        _update(task_id, 92, "Generating translated PDF...")

        output_pdf = os.path.join(task_dir, "output.pdf")
        target_script = target_lang.split("_")[1] if "_" in target_lang else "Latn"
        text_to_pdf(translated_texts, output_pdf, target_script)

        _update(task_id, 100, "Translation complete!")

    except Exception as e:
        _update(task_id, 0, "Error", error=str(e))
