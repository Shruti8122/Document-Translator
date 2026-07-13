import io
import numpy as np
from PIL import Image

_reader = None


def get_reader(lang_list):
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(lang_list, gpu=True)
    return _reader


def ocr_image(image_bytes: bytes, lang_codes: list) -> str:
    reader = get_reader(lang_codes)
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)
    results = reader.readtext(image_np)
    text_lines = [line[1] for line in results]
    return "\n".join(text_lines)
