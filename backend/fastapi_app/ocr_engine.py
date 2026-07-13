import io
import numpy as np
from PIL import Image

_readers = {}


def get_reader(lang_list):
    key = tuple(sorted(lang_list))
    if key not in _readers:
        import easyocr
        _readers[key] = easyocr.Reader(list(key), gpu=True)
    return _readers[key]


def ocr_image(image_bytes: bytes, lang_codes: list) -> str:
    reader = get_reader(lang_codes)
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)
    results = reader.readtext(image_np, paragraph=True, detail=0)
    return "\n".join(results)
